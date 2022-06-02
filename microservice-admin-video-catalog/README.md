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

# working with pdm to manage dependencies
pdm init # initializat pdm
pdm add autopep8 # add library
pdm remove autopep8 # remove library
pdm add autopep8 --dev # add library on dev environment

autopep8 --in-place --recursive ./src/ # format itens

```

**Tests**
```bash
python3 -m unittest discover ./src/
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

## Concepts
### Domain
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


### Object Values
On programming we have some types like str, Object, int,...
but when we are talking about domain we need more semantics types

entity = set of attributes + entities + object value

ex: colored pencil
a child is drawing on a paper with a blue colored pencil
and suddenly this pencil breaks, the child can take a blue
pencil from another brand as long as it is the same color.

that's the concept of a object value, doesn't have and id, it has properties
the pencil dosen't has a identification, what matters for us is the color.

ex: Address

an object value must be immutable and equal to another OV if has the same values

### Repository
Responsible for persist the entity data on a database
- stateless


## TO DO
- [ ] Create docker environment (Docker & IDE)
- [ ] Create category entity
- [ ] Create entity tests
- [ ] Create use cases and repositories
- [ ] Create use cases tests
_____ Replicate to others entities (Genre, Cast member,...)


- [ ] Set up (REST API)
- [ ] Integrate with RabbitMQ and Encoder Video
- [ ] E2E Tests