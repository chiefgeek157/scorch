# scorch
**SCO**recard for a**RCH**itecture provided s web-based scorecard system for Enterprise Architecture.

After decades of service as an Enterprise Architect including starting up EA programs, taking over eisting EA programs, and as a senior
excecutive for EA in companies large and small, the creator of scorch found a consistent need has been to assess existing application ecosystems for
adherence to well-known principles.

Whether in a technology shop or the IT department of a company in a non-technology business, reality is the same. Technology team face the
same contracints of time, resources, and schedule and have to make trade-offs resulting in the accumulation of technical debt.

The scorch project provides a means to define a collection of rules that capture what we "should" do so we can objectively compare that to
what we actually did. No judgement on people, who are usually doing the best they can with what they have, but, rather, a bright
objective light on the system itself to measure what is good and what could be better.

Critically, scorch provides two objective measures that in the cuthor's estimation provide the means to change behavior in the moments when
it counts most: at the points of funding and proiritization:

* Measure of risk expressed as a "health score"
* Estimation of cost, to bring the health score to ideal

# Setup

scorch uses `django-environ` to help simplify configuration. Developers should copy the `scorch/.env.smaple` file to `scorch/.env` and modify.
Note that the `.env` file should ***not*** be checked into source control because it contains secrets such as
`SECRET_KEY`.

The `scorch/project/settings.py` file is a typical Django settings file but sets environment-specific values from the `.env` file. `.env.sample` contains
the set of variables that `settings.py` will use, bu default. Developers are free to modify these files as needed
to suit a particular installation.

## Creating default users

The `account` app provides a custom command to create the default Groups and Users needed. To run:

```
$ python manage.py create_groups
```

The command is idempotent so only makes changes that are needed.