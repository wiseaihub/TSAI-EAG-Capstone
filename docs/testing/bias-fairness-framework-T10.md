# Bias & Fairness Assessment Framework (T10)

## Demographic Dimensions
| Dimension | Sub-groups |
|-----------|-----------|
| Gender | Male, Female, Other |
| Age group | Paediatric, Adult, Elderly |
| Geography | Urban, Rural, Tribal |
| Language | Hindi, Telugu, Tamil, English |
| Socioeconomic | BPL, APL |

## Fairness Metrics
- Equal Accuracy across groups (target: < 5% delta between any two groups)
- Calibration: confidence scores consistent across groups
- No disparate impact on any sub-group vs overall

## Test Protocol
- Stratified dataset with demographic metadata
- Run model per sub-group independently
- Report disaggregated metrics
- Escalate if delta > 5% on any group

## Links
- Execution: T52 (Bias testing sprint)
- Final report: T75
