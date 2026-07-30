# PR review emoji legend

Use one leading emoji on every posted PR finding and overall review verdict. A
stable mapping makes disposition scannable and prevents reviewers from inventing
conflicting severity markers. If repository defines its own review vocabulary or
emoji, follow repository policy instead.

## Per-comment severity

| Emoji | Meaning    | When to use                                                                                                    |
| ----- | ---------- | -------------------------------------------------------------------------------------------------------------- |
| 🐛    | Blocking   | Must be fixed before merge: correctness, security, data loss, broken contract, or missing required validation. |
| ⚠️    | Important  | Real maintainability, reliability, documentation, or coverage concern worth fixing now or explicitly tracking. |
| 📝    | Suggestion | Optional improvement, nitpick, or style preference. Never blocks merge alone.                                  |
| ❓    | Question   | Clarification is needed before issue can be judged. Not yet a confirmed defect.                                |
| 👍    | Praise     | Optional recognition of something done particularly well.                                                      |

## Overall review verdict

| Emoji | Verdict         | When to use                                                                                                                                        |
| ----- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🎉    | Approve         | No blocking findings remain open. Important, suggestion, or question findings may remain if repository policy permits approval.                    |
| 🛑    | Request changes | At least one blocking finding remains open.                                                                                                        |
| 💬    | Comment         | Findings exist but no blocking defect is confirmed, and approval is not appropriate yet. Use sparingly while awaiting clarification or validation. |

## Mechanics

- Put marker at start of posted comment body: `🐛 <finding>`.
- Put verdict marker at start of submitted review body: `🎉 <summary>`.
- Use one disposition emoji per comment. Do not decorate remaining text with extra
  emoji; marker should stay unambiguous.
- If severity changes after discussion, edit or reply to original finding so stale
  marker does not misrepresent current disposition.
- A question with independently established blocking risk remains 🐛; phrase body
  as question if clarification is still needed.
