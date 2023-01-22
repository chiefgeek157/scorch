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
    'skinparam linetype ortho
    ' cannot use linetype ortho because it moves labels
    ' https://forum.plantuml.net/15405/broken-class-diagram-when-linetype-set-to-ortho?show=15405#q15405
    !pragma layout elk

    package Entities <<Frame>> {
        entity EntityType {
            * name : string
        }

        entity Entity {
            * id : string
            * name : string
        }

        EntityType "is of" ||--o{ "has" Entity

        package Attributes <<Frame>> {
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
            EntityType "is for" ||--o{ "defines" Attribute
        }
    }

    package Scorecards <<Frame>> {
        entity Scorecard {
            * name : string
        }

        entity ScoreRating {
            * order : int
            * label : string
            * score : float
            * min_score : float
        }
        Scorecard "is for" ||--o{ "has" ScoreRating

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

        package Scorecard_Versions <<Frame>> {
            entity ScorecardVersion {
                * label : version string
            }

            entity ScoreItemVersion {
            }
            Scorecard "is of" ||--o{ "has" ScorecardVersion
        }

        EntityType "is for" ||--o{ "has" Scorecard


        Entity "has" ||--o{ "describes" AttributeValue
        Attribute "has" ||--o{ "is of" AttributeValue


        Scorecard "is part of" ||--o{ "defines" ScoreItemType
        ScoreItemType "has parent" ||--o{ "has child" ScoreItemType
        ScoreItemType "has" ||--o{ "is of" ScoreItem
        Attribute "is used by" }o..o{ "references" ScoreItem
        AttributeValue "is used by" }o..o{ "references" ScoreItem

        ScorecardVersion "uses" }|--|{ "is used by" ScoreItemVersion
        ScoreItem "has" ||--o{ "is of" ScoreItemVersion
        ScoreItemVersion "uses" }|--|{ "is used by" ScoreItemVersion
    }

    package Responses <<Frame>> {
        entity Response {
            scored_on : date
            scored_by : string
            reviewed_on : date
            reviwed_by : string
        }

        entity ScoreItemResponse {
            * score : float
            * score_rating : <<Fk>>
            * comment : string
        }

        entity Task {
            * name : string
            * description : string
            * min_expense : float
            * max_expense : float
            * min_effort : float
            * max_effort : float
        }

        Entity "has" ||--o{ "is for" Response
        ScorecardVersion "has" ||--o{ "of" Response
        Response "has" ||--o{ "is part of" ScoreItemResponse
        ScoreItem "has" ||--o{ "is for" ScoreItemResponse
        ScoreRating "is used by" ||--o{ "has" ScoreItemResponse

        Response "has" ||--o{ "is for" Task

        ScoreItemResponse "has" }o--o{ "applies to" Task
    }
@enduml
```
