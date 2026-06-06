# Design Notes – SentraGuard Lite

## Problem Statement

The goal of this project was to develop a lightweight guardrails gateway that can check for prompts before they pass to a language model.

The system is based on the detection of 3 major categories of risk:

* Prompt Injection
Personally Identifiable Information (PII)
* RAG Injection

The gateway analyses the risks detected, computes a risk score and provides a recommendation for action.

---

## Detection Approach

The idea for this assignment was to use a rule-based approach rather than a machine-learning based solution.

These were primarily due to:

* Simpler implementation
* Faster execution
* Easier debugging
This is determined by the instructions you follow in your test, ensuring that it only depends on your own execution.

Because the assignment was a concept-based exercise for guardrails, rather than one on model training, a pattern matching approach was appropriate.

---

## Technology Choices

### FastAPI

The choice of FastAPI was made due to the following features:

* Automatic request parameter validation using Pydantic.* Automatic validation of request parameters using Pydantic.
* Built-in API documentation
* Simple endpoint creation
* Lightweight deployment

The framework allowed the API layer to remain small and easy to maintain.

### Streamlit

The implementation of Streamlit was opted for the creation of a simple user interface that does not require a separate framework on the front end.

This enabled quick to generate working interface for prompt testing and display the analysis results.

### Docker

Docker support was added to support the Application's ability to run consistently in various environments without a manual dependency installation.

---

## Risk Scoring Design

A scoring model was put in place with weights.

When a detector fires a predetermined score is added:

| Risk Type        | Score |
| ---------------- | ----- |
| Prompt Injection | 50    |
| PII              | 30    |
| RAG Injection    | 40    |

The total of the risks which are detected is the final score.

This was selected for a number of reasons including that is a relatively easy approach to explain, test and modify.

---

## Decision Policy

There are presently three decision levels:

| Score Range | Decision  |
| ----------- | --------- |
| 0 – 39      | Allow     |
| 40 – 79     | Transform |
| 80+         | Block     |

Using this policy, a moderate risk prompt will continue to be expressed after sanitization has been applied, and a highly suspicious prompt will not be expressed.

---

## Tradeoffs

A number of compromises were considered in the development.

### Simplicity vs Coverage

The system focus is simplicity, rather than maximum detection coverage.

More sophisticated could see more attacks but would be more difficult and require more maintenance.

### Explainability vs Intelligence

Pattern-based detection—gives results that are easy to explain.

Logically more advanced methods based on machine learning can be used to increase the accuracy of the detected information, but they would be less transparent and consume more specialists.

---

## Limitations

So far the current implementation has some known limitations:

Patterns can only be detected if they are pre-defined.
Only email address and Customer Number/Phone Numbers are considered as PII.
Context analysis relies on one of the keyword-match approach.
There are no authentication mechanism in place.
It doesn't come with any persistent storage or audit logging.

These restrictions have been allowed to ensure that the scope is in line with the requirements of the assignment.

---

## Future Improvements

Possible future improvements:

* Machine-learning-assisted detection
* Additional PII categories
* Configurable scoring policies
Authorizing and controlling access to the data 9.Authorisation and access control 9.
* Audit logging
* Historical analysis dashboards

---

## Testing Strategy

Automated tests with positive and negative scenarios are included in the project.

Testing focuses on:

* API behaviour
* Detector functionality
* PII redaction
* Risk scoring
* Response validation
Handling special cases like blank prompts

This facilitates faster verification of changes, without manual testing.