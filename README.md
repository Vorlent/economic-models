# economic-models

This is a collection of economic models:

# Pure Circulation

"Pure Circulation" is an equilibrium model where people allocate their income towards consumption or saving.
All income is spent, therefore there is no inflation or deflation in this model.
People have a desired maximum amount of savings/debt, if they are below this then they will save/borrow
until they reach it.
Borrowing does not add to aggregate income. This means all borrowed money has to come from someone
who is intending to save money in this round.

If there are more savers than borrowers or more borrowers than savers, savings or borrowed money will be rationed
based on how much someone wants to borrow or save. Money that cannot be saved because no borrower could be found
will have to be diverted back to consumption again. Money that has been borrowed, always adds to consumption.

When there is an oversupply of goods, the price is lowered until they can all be bought. If there is a
shortage of goods, then the price is raised until no income is left over. Aggregate demand and aggregate supply
are in equilibrium. People who are more productive get proportionally more income.

These assumptions are of course wildly unrealistic but without simplification it would take decades to develop
a model that accurately reflects the real world. This doesn't mean that these models are aspirational models
of how we should structure our economy. They are just an attempt by someone with limited time to build something at all.

Note that this is trying to mimic your average neoclassical economic model based on very crude internet research by
someone who is not an economics student. The main difference between a model based on differential equations is that
this a pseudo agent based model. The system divides global income, global savings and global debt into local income,
local savings and local debt, but equilibrium is determined globally instead of using local rules on the agent level.

Run the model with:

```
./gradlew runPureCirculation
```

Ideas for the next model:

* Model cash savings
* Model interest payments and bonds
* Model multiple goods consumption and production
* Model multi step production