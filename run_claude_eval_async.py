import os
import asyncio
import pandas as pd
from anthropic import AsyncAnthropic
from datetime import datetime, timezone

# Initialize the ASYNC client
client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Limit concurrent requests to 4 at a time to prevent 429 Rate Limits
SEMAPHORE = asyncio.Semaphore(4)
FILE_LOCK = asyncio.Lock()

async def process_single_row(row_data, output_file, language_name):
    # Retrieve using the mapped column names
    pid = row_data.get('prompt_id')

    # Skip invalid rows
    if pd.isna(pid):
        return

    async with SEMAPHORE:
        try:
            # Use the mapped prompt_text
            prompt = row_data.get('prompt_text')
            if pd.isna(prompt):
                print(f"⚠️ Skipping row {pid}: No prompt text found.")
                return

            # Make the asynchronous API call
            response = await client.messages.create(
                model=os.environ.get("CLAUDE_MODEL", "claude-opus-4-8"),
                max_tokens=4096,
                messages=[{"role": "user", "content": str(prompt)}]
            )

            # Extract response details
            result_text = response.content[0].text
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            # Construct the 10-column schema
            processed_row = pd.DataFrame([{
                "prompt_id": pid,
                "language": language_name,
                "category": row_data.get("category", ""),
                "prompt_text": prompt,
                "response_text": result_text,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "stop_reason": response.stop_reason,
                "model": os.environ.get("CLAUDE_MODEL", "claude-opus-4-8"),
                "timestamp_utc": datetime.now(timezone.utc).isoformat()
            }])

            # Append safely
            async with FILE_LOCK:
                header_needed = not os.path.exists(output_file) or os.path.getsize(output_file) == 0
                processed_row.to_csv(output_file, mode='a', header=header_needed, index=False)

            print(f"✅ Successfully processed row {pid}")

        except Exception as e:
            print(f"❌ Error processing row {pid}: {e}")

async def main():
    os.makedirs("output", exist_ok=True)

    files_to_run = [
        ("data/romanized_hindi_split.csv", "output/romanized_hindi_split_output.csv", "Hindi"),
        ("data/romanized_telugu_split.csv", "output/romanized_telugu_split_output.csv", "Telugu"),
        ("data/romanized_kannada_split.csv", "output/romanized_kannada_split_output.csv", "Kannada")
    ]

    for input_path, output_path, lang in files_to_run:
        if not os.path.exists(input_path):
            print(f"⚠️ Skipping {input_path} (File not found)")
            continue

        print(f"🚀 Kicking off async run for: {input_path}")
        df = pd.read_csv(input_path)

        # Map your columns to the expected names
        df = df.rename(columns={
            'romanized_query': 'prompt_text',
            'message_id': 'prompt_id'
        })

        # Ensure category column exists
        if 'category' not in df.columns:
            df['category'] = ""

        tasks = [process_single_row(row, output_path, lang) for _, row in df.iterrows()]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
