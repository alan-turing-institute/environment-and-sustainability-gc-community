# Environment and Sustainability Grand Challenge - Community Repo

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11167969.svg)](https://doi.org/10.5281/zenodo.11167969)

Welcome to the Community repo for the Turing Environment and Sustainability Grand Challenge (E&S GC). This repository contains open materials developed by and for the E&S GC. We invite you to review our activities and contribute where you can!

## The Problem 
High-impact environmental events such as heatwaves, flooding and droughts are increasing in both frequency and magnitude. This threatens our planet, including the four billion people who live in cities and the rich biodiverse natural ecosystems from which life on earth relies on. 

To act on this we need to slow the pace of global heating, predict and mitigate climate impacts, and provide clear evidence to develop national and international policy to meet net zero targets.  

**We need to rapidly develop and disseminate best practice for reproducible, ethical and collaborative data science, along with pathways for impact, leadership and community-lead mission development.**

## The Solution
**At The Alan Turing Institute, we believe collaborative data science to be one of the most impactful ways to address this challenge, and that collaborative data science is best achieved through open research community management.**

### What is open research community management?

A community (or Community of Practice) is a group of people with a shared interest or skill, who work together to collectively forward a mission. This community operates under the broad mission to use data science to address the climate and biodiversity crisis and the need for greater sustainability.

Community managers identify and scaffold meaningful pathways for everyone to gain access to the skills and resources they need to participate in the community. They invest in engaging, training and empowering a diverse group of members such as researchers, research engineers, programme/project management and the business side of the organisation. They foster diverse Communities of Practice within specific expertise in EDI and open research, and they advocate for the needs of community members at all levels. 

Learn more about [Research Community Management at Turing](https://github.com/alan-turing-institute/open-research-community-management.)

## What are we doing?
The following activities are form the E&S specific objectives of our RCM ([Cassandra Gould van Praag])(http://turing.ac.uk/people/researchers/cassandra-gould-van-praag) for the year to Summer 2024. These objectives are a direction of travel, which we will work to evidence progress towards. You can review the full [objectives document in the roadmap direcory](./roadmap/objectives-srcm.md).

### Objective 1: Community strategy
- **Activity**: Use systematic stakeholder mapping to record/identify stakeholders in the E&S GC across all sectors, and classify them according to engagement and community readiness. Develop strategy for growth and engagement in targeted areas. 
- **Value**: An effective community strategy will enable the design and delivery of impactful activities associated with the E&S GC, which are well-grounded in the needs of the community. Meaningful engagement will add to the sustainability of the GC and community activities through increased stakeholder buy-in, equitable participation, and the development of leadership opportunities. 

**UPDATE: Review progress against this objective in pur [community strategy doc](./roadmap/community-strategy.md)**


## Objective 2: Community resources
- **Activity**: Develop and share E&S community documentation and activities to develop plans for embedding open science and reproducibility in E&S.
- **Value**: High quality community documentation and engagement opportunities will support community members to meaningfully engage with the E&S GC, and encourage sustained participation through positive and equitable experiences. 

**UPDATE: To push changes to the handbook:** 
*Admin should ensure that the github pages settings for the repo are set to build with the source `branch`; branch `gh-pages` `/docs`.*

Pull this repo and make your edits to files in `/docs`, then:
1. `pip install -r docs/requirements.txt`
2. `jupyter-book build docs`
3. Follow the onscreen instructions to view a local copy of the html for the book. I use "paste this line directly into your browser bar:" address. Check everything looks good!
4. `ghp-import -n -p -f docs/_build/html` to make a branch called `gh-pages` and push the newly built HTML to the `gh-pages` branch.
5. `git add .` add all changes to the staging area
6. `git commit -m "[commit message for your changes]"` add a relevant commit message for the changes made
7. `git push`
8. View the updated handbook at [https://alan-turing-institute.github.io/environment-and-sustainability-gc-community/](https://alan-turing-institute.github.io/environment-and-sustainability-gc-community/)

Note there is a workflow [book.yml](/.github/workflows/book.yml) I've tried to get working for this, but haven't managed to crack it yet! It is currently [disabled in the repo settings](https://docs.github.com/en/actions/using-workflows/disabling-and-enabling-a-workflow#disabling-a-workflow)

## Objective 3: Community engagement in Y2 mission development
- **Activity**:Leading the community engagement and implementation plan to develop E&S missions and roadmap for the next funding period (Y2).
- **Value**: A community-informed mission will enable the identification of areas of strength and ambition for research, and potential for coordinated impact.

## Objective 4: Advocacy
- **Activity**:Represent and communicate Turing’s E&S and community initiatives on professional (national and international) platforms, connecting communities from the broader data science ecosystem. Advocate internally and externally for our key Turing communities: [Tools, Practices and Systems](https://www.turing.ac.uk/research/research-programmes/tools-practices-and-systems), [The Turing Way](http://the-turing-way.netlify.app/), [RCM Team](https://github.com/alan-turing-institute/open-research-community-management).
- **Value**: Successful advocacy of our activities in all sectors will encourage broad and impactful engagement, by attracting stakeholders with aligned values, resourcing and expertise.


## Objective 5: Internal ways of working
- **Activity**: Aligning and operationalising ways of working to support engagement with and involvement of different core capabilities, research teams and business teams within the GC. Facilitate translation of practices and values between teams, to reduce friction and create leadership opportunities. Prioritize transparency and building trust among disparate teams. 
- **Value**: Clear and agreed upon ways of working will support the team to engage with each other efficiently, effectively, and with trust.

## What do we need?
A core framework in our RCM practice is the [Mountain of Engagement](). This describes how we group and strategies for different members of our community based on their community readiness - how active they are in community collaboration, or how active they would like to be. We are currently focused on two key areas of the mountain: the Discovery layer and Sustained participants. 

![The Mountain of Engagement describes how we scaffold the movement of community members from first discovery into leadership](./images/moe-tric.png)

We want to grow awareness of our work to identify as many individuals as possible who are a good fit for our mission and values. We also want to work with individuals who have already signalled that they are keen to engage with our work. We recognise that sustained participation and the move towards leadership may not be easy for everyone to prioritise, so we want to miximise the value for those who are currently able to commit to this work in some way, while we develop strategies to make sustained participation easier for more a diverse set of individuals. 

**If you are interested in any of the work of this community, we encourage you to make yourself known! The easiest way to do this is to add yourself to our [stakeholder map](https://cassgvp.kumu.io/alan-turing-institute-environment-and-sustainability) - see the [form linked on the right of the map](https://forms.office.com/e/ws9EHtiLkV)** 

**If you know already that you have the capacity and motivation for some degree of leadership or direction setting in this community, please email our RCM so we can learn more about your activities and ambitions: Contact cgouldvanpraag@turing.ac.uk**

## Who are we?
This material has been prepared by the Turing E&S GC Senior Research Community Manager, [Cassandra Gould van Praag](http://turing.ac.uk/people/researchers/cassandra-gould-van-praag). Cassandra is supported under the leadership of the Turing [Tools, Practices and Systems Programme](https://www.turing.ac.uk/research/research-programmes/tools-practices-and-systems). The delivery of all community work is supported by the leadership and operations team of the E&S GC.

## Contact us
Contact our RCM directly to ask questions, strategise and daydream about possibilities - I love to  hear about your work and think of ways we can support each other! Email cgouldvanpraag@turing.ac.uk

### Slack
You can request to be added to the Turing E&S Slack when you [add yourself to our stakeholder map](https://forms.office.com/e/ws9EHtiLkV). If you do not wish to appear on the stakeholder map, you can [request access to slack only using this form](https://forms.office.com/e/fDnC5pR9Zc).

In slack, please introduce yourself on the #welcome channel, and feel free to send a direct message to Cass @cassgvp!

## Citation and acknowledgements
Please cite this material as below:

> Cassandra Gould van Praag. (2024). alan-turing-institute/environment-and-sustainability-gc-community. Zenodo. https://doi.org/10.5281/zenodo.11167968

As contributors to this material grow, we will discuss and and agree a convention for attribution in the citation following the conventions of The Turing Way.

### Acknowledgements
This material has been prepared incorporating guidance and best practice from The Turing Way.

> The Turing Way Community. (2022). The Turing Way: A handbook for reproducible, ethical and collaborative research (1.0.2). Zenodo. https://doi.org/10.5281/zenodo.7625728

Training in Open Research Community Management was delivered through the Open Life Sciences "Open Seeds" programme.

> Freeberg, M., Psomopoulos, F., Pilvar, D., Batut, B., & Community, O. L. S. (2023). Open seeds by OLS: A mentoring & training program for open science ambassadors. https://f1000research.com/posters/12-710

The community handbook structure was modelled on the [TRIC-DT knowledge commons](https://github.com/alan-turing-institute/tric-dt/issues/6)

