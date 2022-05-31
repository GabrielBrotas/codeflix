## How to run

**Remote Container**
requirements:
- Extensions: Remote Container
```bash
# 1 - open settings (cmd + p)
#   >Remote-Containers: Open Folder in Container...
#   >Click OK
#   >From 'docker-compose.yaml'
# Obs. After the first setup we can rebuild by using >Remote-Container: Rebuild and Reopen in Container
```

**Tests**
```bash
# python3 -m unittest <test path>
python3 -m unittest src.category.tests.unit.domain.test_unit_entities
```

# Layers
**The Clean Architecture**

## Entities - Nivel 0
Responsible to validate the business rules.
These entities are independent of framework/technology, is an object that will help us to ensure our application will behave in the properly way;
These entities will contain our business rules;
*This is not anemic entity*

## Use Cases - Nivel 1
Will be responsible to execute the business rules together with the entities;

## Controllers - Nível 2
Will be responsible to call the use cases, if the controller change the protocol (http, grpc, graphql,...) or the client (web,mobile) these change shouldn't affect our use cases and our entities;


```
[ Controller [ Use Cases [ Entities ] ] ]
```

Whenever an inner layer changes the outer layers tend to change;
Usually the outer layers tends to change more than the inner layers because the inner layers are more stable;

## Domain
Understanding the catalog core domain.

```
                [ Aggregates ]   
[Category] - [ Genre ] - [Cast Member] - [Video]
```

Usually nouns tends to become entities/aggregates;

We just need to worry about framework on the last layer
Aggregates -> Language
Use Cases -> Language
Application/Controller -> Framework

## TO DO
- [ ] Create docker environment (Docker & IDE)
- [ ] Create category entity
- [ ] Create entity tests
- [ ] Create use cases and repositories
- [ ] Create use cases tests
_____ Replicate to others entities (Genre, Cast member,...)


- [ ] Set up Nest.js (REST API)
- [ ] Integrate with RabbitMQ and Encoder Video
- [ ] E2E Tests