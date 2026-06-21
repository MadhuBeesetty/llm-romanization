# Romanization Evaluation Results

| file                                           | rows | invalid_rows | query_bge | response_bge | query_bert_f1 | query_bert_precision | query_bert_recall | response_bert_f1 | response_bert_precision | response_bert_recall | llm repeated query | llm repeated response | native_text_in_query | native_text_in_response |
| ---------------------------------------------- | ---: | -----------: | --------: | -----------: | ------------: | -------------------: | ----------------: | ---------------: | ----------------------: | -------------------: | -----------------: | --------------------: | -------------------: | ----------------------: |
| anthropic_romanized_hindi_scored               |  142 |            0 |     0.801 |        0.837 |         0.669 |                0.640 |             0.702 |            0.676 |                   0.644 |                0.711 |                  0 |                     0 |                    0 |                       0 |
| anthropic_romanized_kannada_scored             |  142 |            5 |     0.711 |        0.733 |         0.621 |                0.592 |             0.654 |            0.620 |                   0.588 |                0.657 |                  0 |                     0 |                    1 |                       5 |
| anthropic_romanized_telugu_scored              |  142 |            4 |     0.767 |        0.789 |         0.664 |                0.637 |             0.693 |            0.671 |                   0.641 |                0.705 |                  1 |                     0 |                    1 |                       3 |
| gemini_romanized_hindi_scored                  |  142 |           10 |     0.700 |        0.763 |         0.598 |                0.571 |             0.628 |            0.617 |                   0.587 |                0.650 |                  1 |                     0 |                    2 |                       8 |
| gemini_romanized_kannada_scored                |  142 |           19 |     0.627 |        0.664 |         0.550 |                0.525 |             0.578 |            0.569 |                   0.541 |                0.601 |                  0 |                     1 |                    3 |                      18 |
| gemini_romanized_telugu_scored                 |  142 |           25 |     0.600 |        0.630 |         0.532 |                0.509 |             0.557 |            0.548 |                   0.524 |                0.576 |                  0 |                     0 |                   10 |                      24 |
| gpt_romanized_hindi_scored                     |  142 |            0 |     0.769 |        0.828 |         0.647 |                0.617 |             0.680 |            0.663 |                   0.632 |                0.699 |                  0 |                     0 |                    0 |                       0 |
| gpt_romanized_kannada_scored                   |  142 |            2 |     0.714 |        0.749 |         0.627 |                0.599 |             0.658 |            0.641 |                   0.610 |                0.677 |                  0 |                     0 |                    0 |                       2 |
| gpt_romanized_telugu_scored                    |  142 |            0 |     0.760 |        0.794 |         0.651 |                0.624 |             0.681 |            0.667 |                   0.637 |                0.700 |                  0 |                     0 |                    0 |                       0 |
| ollama_romanized_hindi_split_scored            |  142 |            4 |     0.735 |        0.787 |         0.622 |                0.595 |             0.653 |            0.639 |                   0.609 |                0.672 |                  3 |                     3 |                    0 |                       0 |
| ollama_romanized_kannada_improved_split_scored |  142 |           20 |     0.577 |        0.537 |         0.514 |                0.485 |             0.552 |            0.549 |                   0.577 |                0.534 |                  5 |                    19 |                    0 |                       0 |
| ollama_romanized_telugu_split_scored           |  142 |           16 |     0.584 |        0.598 |         0.577 |                0.583 |             0.578 |            0.574 |                   0.593 |                0.568 |                 12 |                    16 |                    0 |                       0 |

## Notes

* `invalid_rows` = rows where:

  * query_en and query_roman overlap = 1, OR
  * response_en and response_roman overlap = 1, OR
  * native script text detected in query, OR
  * native script text detected in response.

* `llm repeated query` = model returned the original query without romanization.

* `llm repeated response` = model returned the original response without romanization.

* `native_text_in_query` = query output contains at least one native-script character.

* `native_text_in_response` = response output contains at least one native-script character.
