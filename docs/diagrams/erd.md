ER diagram of the scorch model.

A Scorecard is the central focus if scorch. Scorecards define a collection
of ScoreItems, which are the things that people evaluate to create a score.
ScoreItemTypes are organized in to a hierachy for a given Scorecard.

For example, for Scorecard used for an application EntityType, the
ScoreItemTypes might be:

- Objective: a high-level business goal for every application. Examples include
Safety, Flexibility, and Cost-Effectiveness
    - Principle: a characteritic of applications that achieve the parent
Objective. For example, Secure might be a Principle under Safety.
        - Directive: a way that an application achieves the characteristic
stated in the Principle. A directive might state something like,
"Scan code for vulnerabilities."
            - Rule: a scorable statement about the application.

Entities are the architectural entities being scored by a Scorecard.
Each entity type can have multiple Scorecards

```plantuml
@startuml test1
    skinparam backgroundColor #EEEBDC
    ' avoid problems with angled crows feet
    skinparam linetype ortho

    entity EntityType {
        * name : string
    }

    entity Entity {
        * id : string
        * name : string
    }

    entity Attribute {
        * name : string
        * type : enum
    }

    entity AttributeValue {
        * value_string : string
        * value_int : int
        * value_bool : bool
        * value_float : float
    }

    entity Scorecard {
        * name : string
    }

    entity ScoreRating {
        * order : int
        * label : string
        * score : float
        * min_score : float
    }

    entity ScorecardVersion {
        * label : version string
    }

    entity ScoreItemType {
        * name : string
        * scorable : bool
    }

    entity ScoreItem {
        * name : string
        * description : string
        * owner : string
        * weight : float
        * weight_formula : string
        * importance_formula : string
    }

    entity ScoreItemVersion {
    }

    entity Response {
        scored_on : date
        scored_by : string
        reviewed_on : date
        reviwed_by : string
    }

    entity ScoreItemResponse {
        * score : float
        * score_rating : string
        * comment : string
    }

    EntityType "has" ||--o{ "is of" Entity
    EntityType "has" ||--o{ "is for" Scorecard

    Scorecard "has" ||--o{ "is of" ScorecardVersion

    Scorecard "defines" ||--o{ "is for" Attribute
    Entity "has" ||--o{ "describes" AttributeValue
    Attribute "has" ||--o{ "is of" AttributeValue

    Scorecard "is part of" ||--o{ "defines" ScoreItemType
    ScoreItemType "has parent" ||--o{ "has child" ScoreItemType
    ScoreItemType "has" ||--o{ "is of" ScoreItem
    Attribute "is used by" }o..o{ "references" ScoreItem
    AttributeValue "is used by" }o..o{ "references" ScoreItem

    ScorecardVersion "uses" }|--|{ "is used by" ItemVersion
    'ItemVersion "is for" }o--|| "has" Item
    ScoreItem "has" ||--o{ "is of" ScoreItemVersion
    ScoreItemVersion "uses" }|--|{ "is used by" ScoreItemVersion

    Entity "has" ||--o{ "is for" Response
    ScorecardVersion "has" ||--o{ "of" Response
    Response "has" ||--o{ "is for" "ScoreItemResponse"
@enduml
```
After