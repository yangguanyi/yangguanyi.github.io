# Research records for Guanyi Yang's academic website.
# Paper abstracts are preserved from the published or explicitly dated source.
# Separate explanatory fields were checked against the complete source PDFs.
# Update a record and its reviewed_on date when its scholarly content changes.

PAPERS = [{'slug': 'dark-skies-great-sand-dunes',
  'kind': 'article',
  'theme': 'night-sky',
  'title': 'Contingent Behavior Modeling for Dark Skies Valuation at Great Sand Dunes National Park',
  'authors': [('Mark Eiswerth', 'University of Northern Colorado; Colorado College'),
              ('Liam Mullen', 'Colorado College'),
              ('Guanyi Yang', 'Colorado College')],
  'year': 2026,
  'venue': 'American Journal of Agricultural Economics',
  'venue_detail': '2026, pp. 1–25 (accepted 28 April 2026)',
  'doi': '10.1002/ajae.70080',
  'jel': ['Q26', 'Q51', 'Q56'],
  'keywords': ['contingent behavior model',
               'dark sky conservation',
               'ecotourism',
               'latent class',
               'national park',
               'negative binomial',
               'nightlight pollution',
               'survey methods',
               'tourism',
               'travel cost model',
               'willingness-to-pay'],
  'one_liner': 'An on-site visitor survey and recreation-demand model estimate that suburban levels of '
               'light pollution would reduce visitor consumer surplus at Great Sand Dunes by 23 to 24 '
               "percent. The paper uses each respondent's home night sky to describe a hypothetical "
               'change in environmental quality.',
  'abstract': 'Dark sky conservation is increasingly popular, requiring facility upgrades and community '
              'cooperation. This study assesses its economic benefits at Great Sand Dunes National Park '
              'and Preserve, a Gold Tier International Dark Sky Park. Through on-site surveys, we '
              'collected data on visitor behaviors, expenditures, and night sky perceptions. We '
              'introduced a continuum of contingent night sky brightness levels based on visitors’ home '
              'locations and measured changes in visitation. Our Travel Cost-Contingent Behavior '
              'analysis shows that each unit increase in nightlight decreases visitation by 0.05 days '
              'over 5 years. Using a weighted Latent Class Negative Binomial (LCNB) model, we estimate '
              'consumer welfare losses under escalating nightlight pollution scenarios. If the park’s '
              'night skies matched an average rural, suburban, or urban area, visitors’ consumer '
              'surplus would fall by about 3%, 23–24%, and 42–44%, respectively. These results '
              'underscore the substantial economic value of preserving dark skies.',
  'findings': ['Under hypothetical increases in park nightlight, the weighted model estimates about '
               '0.05 fewer visitor-days per person over five years for each additional unit of VIIRS '
               'radiance, measured in nW/cm²/sr (Table 2).',
               '47 percent of respondents said they would make fewer visits or shorter visits if the '
               "park's night sky matched the sky at home. Average visitor-days were 2.68 in the "
               'historical state and 1.60 in the contingent state (Table 1).',
               'Estimated losses of visitor consumer surplus are about 3 percent under rural '
               'brightness, 23 to 24 percent under suburban brightness, and 42 to 44 percent under '
               'urban brightness. These ranges compare unweighted and weighted models, not confidence '
               'intervals (Table 5).',
               'The suburban-brightness scenario implies annual per-person losses of about $39 in the '
               'unweighted model and $159 in the weighted model. Scaling those estimates to 500,000 '
               'annual visits gives about $19.5 million and $79.3 million. These are modeled recreation '
               'use values, not changes in visitor spending or park revenue (Table 5).',
               'Consumer surplus per visitor-day is $323.95 in the unweighted latent-class model and '
               '$1,226.29 in the weighted model, showing the importance of adjusting for the on-site '
               'sampling of frequent visitors (Table 4).'],
  'limits': ['The analysis uses 330 visitor-party surveys collected at one park over October 20 to 22, '
             '2023. It does not include nonvisitor existence or bequest values.',
             'Future visits are hypothetical responses to a scenario that holds other park attributes '
             'constant. The study does not observe a lighting intervention or establish that '
             'hypothetical bias is absent.',
             'VIIRS upward radiance is not a direct measure of perceived sky brightness and has limited '
             'sensitivity to blue-rich LED light. Travel costs exclude the opportunity cost of travel '
             'time.',
             'Welfare estimates depend on weighting and model assumptions. Aggregate values assume '
             '500,000 annual visits and are not a cost-benefit evaluation of a particular lighting '
             'policy.'],
  'context': ["Each visitor compares the park's night sky with the sky where they live. These "
              'respondent-specific scenarios create a continuous brightness gradient across the sample.',
              'Fixed-effects negative binomial models use historical and contingent visitor-days. '
              'Latent-class models estimate travel-cost responses and consumer surplus, with inverse '
              'visit-day weighting to address the overrepresentation of frequent visitors.',
              'The authors discuss possible applications of personalized scenarios to water quality, '
              'wildfire risk and noise. Those domains are proposed applications, not empirical outcomes '
              'in this study.'],
  'data': 'On-site survey of 367 visitor parties at Great Sand Dunes National Park and Preserve, '
          'Colorado, on October 20 to 22, 2023; 330 enter the analysis. Home ZIP codes are matched to '
          '2022 cloud-free VIIRS nightlight radiance, and park radiance is measured in October 2023.',
  'method': 'Travel-cost and contingent-behavior analysis combining historical visits with responses to '
            'a hypothetical home-sky scenario. Fixed-effects negative binomial models estimate '
            'nightlight responses; latent-class negative binomial models and inverse visit-day weights '
            'estimate recreation consumer surplus while addressing on-site sampling.',
  'whats_new': 'Develops personally familiar, respondent-specific scenarios for valuing continuous '
               'changes in environmental quality, and combines on-site sampling weights with '
               'latent-class recreation-demand models.',
  'audiences': ['Environmental and resource economists working on nonmarket valuation, recreation '
                'demand and on-site sampling corrections',
                'National Park Service staff, park managers and dark-sky program designers',
                'DarkSky International, astrotourism and tourism researchers',
                'Colorado policymakers (HB22-1382, Support Dark Sky Designation and Promotion in '
                'Colorado)',
                'Researchers using satellite nighttime lights'],
  'related': [('Hynes, S. and W. Greene (2013). A panel travel cost model accounting for endogenous '
               'stratification and truncation: a latent class approach. Land Economics 89(1): 177–192.',
               '10.3368/le.89.1.177'),
              ('Hynes, S. and W. Greene (2016). Preference heterogeneity in contingent behaviour travel '
               'cost models with on-site samples. Journal of Agricultural Economics 67(2): 348–367.',
               '10.1111/1477-9552.12143'),
              ('Shi, W. and J. Huang (2018). Correcting on-site sampling bias: a new method with '
               'application to recreation demand analysis. Land Economics 94(3): 459–474.',
               None),
              ('Egan, K. and J. Herriges (2006). Multivariate count data regression models with '
               'individual panel data from an on-site sample. Journal of Environmental Economics and '
               'Management 52(2): 567–581.',
               None),
              ('Heberling, M. T. and J. J. Templeton (2009). Estimating the economic value of national '
               'parks with count data models using on-site, secondary data: the case of the Great Sand '
               'Dunes National Park and Preserve. Environmental Management 43: 619–627.',
               None),
              ('Mitchell, D. and T. Gallaway (2019). Dark sky tourism: economic impacts on the Colorado '
               'Plateau economy, USA. Tourism Review 74(4): 930–942.',
               None),
              ('Simpson, S. N. and B. G. Hanna (2010). Willingness to pay for a clear night sky: use of '
               'the contingent valuation method. Applied Economics Letters 17(11): 1095–1103.',
               None),
              ('Argys, L. M., S. L. Averett and M. Yang (2021). Light pollution, sleep deprivation, and '
               'infant health at birth. Southern Economic Journal 87(3): 849–888.',
               None)],
  'versions': [('Published article (Wiley)', 'https://doi.org/10.1002/ajae.70080'),
               ("Published PDF in the author's repository",
                'https://raw.githubusercontent.com/yangguanyi/Published/main/2026_AJAE_Eiswerth_Mullen_Yang.pdf'),
               ('Working paper version (PDF)',
                'https://github.com/yangguanyi/Working-papers/raw/master/Contingent_Behavior_Modeling_for_Dark_Skies_Valuation_at_Great_Sand_Dunes_National_Park.pdf'),
               ('Policy brief: Tourism Response to Dark Sky Conservation at the Great Sand Dunes (State '
                'of the Rockies, Nov 2024)',
                'https://doi.org/10.52295/dcc.7959'),
               ('Press: CC and UNC Team Research Dark Sky Tourism (The Peak, Jan 2024)',
                'https://thepeak.coloradocollege.edu/2024/01/09/cc-and-unc-team-research-dark-sky-tourism/'),
               ('Essay: The Economics of the Night Sky (State of the Rockies, 2024)',
                'https://www.coloradocollege.edu/other/stateoftherockies/_documents/2024-anthropogenic-article-pdfs/The%20Economics%20of%20the%20Night%20Sky%202024.pdf')],
  'questions': [['How does the study estimate the recreational value of dark skies?',
                 "Visitors describe how their trips would change if the park's night sky looked like "
                 'the sky at home. The authors match those home locations to satellite nightlight and '
                 'use travel-cost and contingent-behavior models to estimate recreation consumer '
                 'surplus.'],
                ['How much would brighter skies affect visitor welfare at Great Sand Dunes?',
                 'The model estimates losses of 23 to 24 percent under suburban brightness and 42 to 44 '
                 'percent under urban brightness. The ranges compare weighted and unweighted '
                 'specifications. They are hypothetical visitor-use values for this park, not '
                 'confidence intervals or observed economic losses.'],
                ['Does the study establish that hypothetical responses are unbiased?',
                 'No. Respondents compare the park with a familiar home sky, and the article examines '
                 'response stability and differences across visitor groups. Those checks do not '
                 'eliminate the possibility of hypothetical bias.']],
  'funding': 'State of the Rockies Project and Hulbert Center for Southwest Studies at Colorado '
             'College; University of Northern Colorado Department of Economics Foundation Fund. NPS '
             'permit GRSA-2023-SCI-0006.',
  'short_summary': 'A visitor survey and recreation-demand model value darker skies at Great Sand Dunes '
                   'and develop personalized scenarios for environmental valuation.',
  'reviewed_on': '2026-11-09',
  'pdf_path': 'papers/dark-skies-great-sand-dunes/paper.pdf',
  'pdf_label': 'Read published paper (PDF)',
  'version_note': 'Summary based on the published article linked here. Earlier working-paper versions '
                  'are listed separately below.',
  'publication_date': '2026-05-10',
  'article_number': 'ajae.70080',
  'online_date': '2026-05-10'},
 {'slug': 'racial-disparities-hiring-discrimination',
  'kind': 'working paper',
  'theme': 'race-macro',
  'title': 'Macroeconomics of Racial Disparities: Discrimination, Labor Market, and Wealth',
  'authors': [['Srinivasan Murali', 'FLAME University'], ['Guanyi Yang', 'Colorado College']],
  'year': 2026,
  'venue': 'Working paper',
  'venue_detail': 'January 2026 manuscript; arXiv 2412.00615v4 posted 23 April 2026',
  'doi': '10.48550/arXiv.2412.00615',
  'arxiv': '2412.00615',
  'jel': ['D14', 'E21', 'J15', 'J64', 'J65'],
  'keywords': ['search-and-matching',
               'heterogeneous agents',
               'hiring discrimination',
               'racial inequality',
               'labor market frictions',
               'unemployment',
               'wage gaps',
               'wealth distribution',
               'business cycles'],
  'one_liner': 'In a U.S.-calibrated search-and-matching model, removing hiring exclusion reduces the '
               "model's black-white unemployment gap by about 57 percent, its average wage gap by 48 "
               'percent, and its median wealth gap by 16 percent. The counterfactual holds racial '
               'differences in job separation, bargaining power, and extreme wealth shocks fixed.',
  'abstract': 'This paper examines the impact of racial discrimination in hiring on employment, wages, '
              'and wealth disparities between black and white workers. Using a labor '
              'search-and-matching model with racially prejudiced and non-prejudiced firms, we show '
              'that labor market frictions sustain discriminatory practices as an equilibrium outcome. '
              'These practices account for 57% of the racial unemployment gap, 48% of the average wage '
              'gap, and 16% of the median wealth gap. Discriminatory hiring also increases unemployment '
              'and wage volatility for black workers, increasing their labor market risks over the '
              'business cycle. Eliminating prejudiced firms reduces these disparities and improves the '
              'welfare of black workers as well as the overall economic welfare.',
  'findings': ['In the steady-state model counterfactual, removing prejudiced firms narrows the '
               'black-white unemployment gap from 7 to 3 percentage points. The mean wage ratio rises '
               'from 0.75 to 0.87, the mean wealth ratio from 0.29 to 0.34, and the median wealth ratio '
               'from 0.33 to 0.44. These close about 57 percent, 48 percent, 7 percent, and 16 percent '
               'of the respective modeled gaps.',
               'Quarterly job-finding probability for black workers rises from 0.49 to 0.64 as '
               "non-prejudiced vacancies replace exclusive vacancies; white workers' probability falls "
               'from 0.66 to 0.64. Racial job-separation rates remain at their benchmark values.',
               'Average consumption-equivalent welfare changes are +12.89 percent for black workers, '
               '-0.48 percent for white workers, and +1.51 percent overall. Individual welfare changes '
               'are averaged using the counterfactual stationary distribution.',
               'Prejudiced vacancies have calibrated posting costs of 4.6314 versus 2.5534 for '
               'non-prejudiced vacancies, but lower job-destruction rates of 0.0268 versus 0.0644. '
               'These type-specific costs and turnover rates allow profitable filled jobs to coexist '
               'while free entry drives the expected value of a new vacancy to zero.',
               'Eliminating hiring exclusion lowers black unemployment volatility relative to output '
               'from 0.26 to 0.18 and the corresponding volatility of the racial unemployment gap from '
               '0.30 to 0.17. The model captures a cyclical mechanism but produces much less '
               'unemployment volatility than observed data.'],
  'limits': ['The gap shares are conditional model counterfactuals, not independent causal estimates of '
             "discrimination's share of observed inequality.",
             'The paper models hiring exclusion. It retains calibrated racial differences in job '
             'separation, bargaining power, and extreme wealth shocks; it does not model a separate '
             'employer rule for wage, promotion, or separation discrimination.',
             'The model includes black and white workers and draws on PSID and CPS data for 1996-2014 '
             'and additional published calibration targets. It understates the median wealth gap: the '
             'modeled black/white ratio is 0.33, versus 0.17 in the cited data.',
             'Unemployment volatility relative to output is much too small in the model: 0.26 for black '
             'workers and 0.22 for white workers, compared with 9.51 and 11.02 in the data.',
             'Welfare results compare stationary equilibria and average individual consumption '
             'equivalents. They are not percentage changes in GDP or a transition-path evaluation of a '
             'specific anti-discrimination policy.',
             'Working paper. This summary was reviewed against the January 2026 manuscript posted as '
             'arXiv v4 on 23 April 2026.'],
  'context': ['Firms represent jobs or vacancies. Prejudiced vacancies exclude black applicants by '
              'assumption; non-prejudiced vacancies accept both groups. Firms use the same technology, '
              'and the model isolates access to opportunities rather than deriving the source of '
              'prejudice.',
              'The counterfactual removes exclusive vacancies and allows endogenous entry of '
              'non-prejudiced vacancies, preserving race-specific benchmark job-separation '
              'probabilities. It does not assume that black and white workers become identical along '
              'every dimension.',
              'Gap shares use modeled baseline denominators. For example, raising the mean black/white '
              'wage ratio from 0.75 to 0.87 closes (0.87 - 0.75)/(1 - 0.75), or 48 percent, of the '
              'initial wage gap to parity.',
              "Welfare is the proportional change in each worker's benchmark consumption stream "
              'equivalent to the change in expected lifetime utility. The paper averages these '
              'individual changes over the counterfactual stationary distribution.',
              'The aggregate-shock extension uses TFP shocks and the Boppart-Krusell-Mitman method '
              'based on small-shock transition responses. This is a heterogeneous-agent search model, '
              'distinct from the separate HANK race project.'],
  'data': 'PSID 1996-2014 for the productivity process, sample composition, and wage-cycle evidence; '
          'CPS 1996-2014 for unemployment cycles; labor-market flow targets from Cajner et al. (2017); '
          'the mean racial wage ratio from Derenoncourt and Montialoux (2021); zero-wealth targets '
          'following Nakajima (2021); 2007 ACS and SCF distributions for validation.',
  'method': 'Quantitative search-and-matching model with two firm types, Nash bargaining with '
            'race-specific bargaining power, unemployment insurance with eligibility, borrowing '
            'constraint, race-specific extreme wealth shocks; steady-state counterfactuals and a '
            'stochastic equilibrium with TFP shocks.',
  'whats_new': 'Connects vacancy-level hiring exclusion to unemployment, wage bargaining, wealth '
               'accumulation, and business-cycle exposure in a calibrated general-equilibrium search '
               'model.',
  'audiences': ['Macro-labor economists and search-and-matching modelers',
                'Economists of discrimination and the racial wealth gap',
                'Federal Reserve and policy researchers on racial disparities over the cycle',
                'Heterogeneous-agent and HANK modelers'],
  'related': [('Nakajima, M. (2023). Monetary policy with racial inequality. Federal Reserve Bank of '
               'Philadelphia Working Paper 23-09 (first version 21-19, 2021).',
               None),
              ('Boerma, J. and L. Karabarbounis (2021). Reparations and persistent racial wealth gaps. '
               'NBER Working Paper 28468.',
               None),
              ('Aliprantis, D., D. R. Carroll and E. R. Young (2023). The dynamics of the racial wealth '
               'gap. Federal Reserve Bank of Cleveland Working Paper 19-18R.',
               None),
              ('Derenoncourt, E., C. H. Kim, M. Kuhn and M. Schularick (2024). Wealth of two nations: '
               'the U.S. racial wealth gap, 1860–2020. Quarterly Journal of Economics 139(2): 693–750.',
               None),
              ('Bertrand, M. and S. Mullainathan (2004). Are Emily and Greg more employable than '
               'Lakisha and Jamal? American Economic Review 94(4): 991–1013.',
               None),
              ('Kline, P., E. K. Rose and C. R. Walters (2022). Systemic discrimination among large '
               'U.S. employers. Quarterly Journal of Economics 137(4): 1963–2036.',
               None),
              ('Cajner, T., T. Radler, D. Ratner and I. Vidangos (2017). Racial gaps in labor market '
               'outcomes in the last four decades and over the business cycle. Federal Reserve Board '
               'FEDS 2017-071.',
               None),
              ('Becker, G. S. (1957). The Economics of Discrimination. University of Chicago Press.',
               None)],
  'versions': [['Reviewed manuscript: arXiv v4, posted 23 April 2026',
                'https://arxiv.org/abs/2412.00615v4'],
               ['Reviewed full text: arXiv v4 PDF', 'https://arxiv.org/pdf/2412.00615v4'],
               ['Latest arXiv listing', 'https://arxiv.org/abs/2412.00615'],
               ('Earlier manuscript, May 2025 (PDF)',
                'https://yangguanyi.github.io/pdf/Murali-Yang-2025-Macroeconomics-of-Racial-Disparities.pdf')],
  'questions': [['How much of the black-white unemployment gap does hiring discrimination explain?',
                 "Removing hiring exclusion reduces the model's unemployment gap from seven to three "
                 'percentage points, about 57 percent. This is a conditional model decomposition that '
                 'preserves racial differences in job separation, bargaining power, and wealth-shock '
                 'probabilities.'],
                ['How can hiring discrimination survive market competition?',
                 'Search frictions create valuable worker-firm matches. In this calibrated model, '
                 'type-specific posting costs and turnover rates permit profitable filled jobs at both '
                 'exclusive and open firms, even though free entry drives the expected value of a new '
                 'vacancy to zero.'],
                ['Can hiring discrimination contribute to the racial wealth gap?',
                 'In the model, job-finding risk and wage bargaining affect saving and wealth '
                 'accumulation. Removing hiring exclusion raises the median black/white wealth ratio '
                 'from 0.33 to 0.44, closing about 16 percent of the modeled gap to parity; the model '
                 'understates the observed median wealth gap.'],
                ['What does the reported welfare gain mean?',
                 'The reported +12.89 percent for black workers and +1.51 percent overall are average '
                 'consumption-equivalent welfare changes between stationary equilibria. They average '
                 'individual changes using the counterfactual population distribution and do not '
                 'measure a uniform increase in consumption, income, or GDP.']],
  'funding': None,
  'publication_date': '2026-01',
  'version_note': 'January 2026 manuscript. The linked PDF is arXiv version 4, posted 23 April 2026.',
  'short_summary': 'A quantitative search model connects hiring discrimination to racial gaps in '
                   'unemployment, wages and wealth.',
  'reviewed_on': '2026-11-09',
  'pdf_path': 'papers/racial-disparities-hiring-discrimination/paper.pdf',
  'pdf_label': 'Read working paper (PDF)'},
 {'slug': 'intermittent-college-enrollment',
  'kind': 'article',
  'theme': 'college-lifecycle',
  'title': 'Better Late Than Never: Macroeconomic Impact of Intermittent College Enrollment and Tuition '
           'Subsidies',
  'authors': [('Guanyi Yang', 'Colorado College')],
  'year': 2025,
  'venue': 'Journal of Economic Dynamics and Control',
  'venue_detail': 'Vol. 181, 105219 (available online 21 November 2025)',
  'doi': '10.1016/j.jedc.2025.105219',
  'jel': ['E2', 'I24', 'J24', 'J31'],
  'keywords': ['heterogeneous agents',
               'incomplete markets',
               'life-cycle model',
               'lifecycle inequality',
               'general equilibrium',
               'labor market risk',
               'human capital accumulation',
               'intermittent enrollment',
               'delayed college completion',
               'college stopout',
               'risk and schooling',
               'self-insurance',
               'consumption-equivalent welfare',
               'tuition subsidies',
               'education policy'],
  'one_liner': 'In a U.S.-calibrated life-cycle model, the option to delay college or return after '
               "leaving accounts for about one quarter of college's total welfare value. Flexible "
               'access is especially valuable for people who begin adult life with fewer resources, '
               'partly because it helps them respond to labor-market risk.',
  'abstract': 'People often delay starting college or temporarily leave college to work. To examine the '
              'welfare implications of intermittent college attendance, I incorporate flexible '
              'age-by-age college enrollment choice in a life-cycle model in general equilibrium. '
              'College serves as an investment device for the young and reduces risk for the old. '
              'Removing flexible access reduces the total welfare value of college by one quarter. '
              'Moreover, higher wealth and better human capital preparedness at age 18 incentivize '
              'early-age degree completion. However, accessing college at a later age matters more for '
              'those who are initially less advantaged. Thus, policies that alleviate financial costs '
              'generate considerable long-term welfare improvements.',
  'findings': ["In the NLSY79 sample, 9.29 percent complete a bachelor's degree by age 22 and 17.03 "
               'percent complete one after a nontraditional path, which includes delayed initial entry '
               'as well as interruption. Among graduates, 16.41 percent finish after age 30. NLSY97 and '
               'CPS cohorts provide checks on later enrollment patterns (Table 1).',
               'Restricting initial enrollment to age 19 and preventing reentry reduces '
               "consumption-equivalent welfare by 3.74 percent and bachelor's attainment by 28.48 "
               'percent relative to baseline. Removing college entirely reduces welfare by 14.77 '
               'percent. The ratio of these welfare losses is about one quarter (Table 6).',
               'Removing flexible access produces larger reductions in degree attainment for people '
               'with low initial wealth or human capital. The roughly 60 percent decline for the lowest '
               'endowment bins is a relative change in BA attainment, not a percentage of all people in '
               'those bins.',
               'In the calibrated decomposition, the investment value of college peaks at 19 and nearly '
               'disappears by 24, while the risk-reduction value emerges after 22 and peaks near 24. '
               'These model-specific ages do not establish an empirical cutoff for adult college '
               'returns.',
               'In a long-run model counterfactual, nationwide free tuition raises BA attainment from '
               '25 to about 78 percent and consumption-equivalent welfare by 39.6 percent, financed by '
               'an 8 percent higher lump-sum tax. Exempting part-time student-workers from labor income '
               'taxes raises attainment by 16.54 percent relative to baseline and average welfare by '
               '1.62 percent, but the lowest initial-human-capital group loses 2.3 percent after taxes '
               'and equilibrium prices adjust.',
               'With a market-based borrowing limit, removing flexible access costs 8.57 percent in '
               'consumption-equivalent welfare, compared with 9.05 percent from removing college '
               'entirely. The importance of flexibility increases under this tighter borrowing '
               'assumption.'],
  'limits': ['U.S. data; the NLSY79 follows cohorts born 1957–1964 (the paper checks NLSY97 and CPS '
             'synthetic cohorts and argues NLSY79 understates intermittence).',
             'The model abstracts from race, gender, geography and industry; a BA is defined as 16 '
             'years of completed schooling.',
             'Baseline uses a natural debt limit; tighter limits are robustness checks. Shocks take two '
             'values to keep computation tractable.',
             'Welfare is measured as consumption equivalence, not financial returns to college.',
             'Policy results are long-run stationary-equilibrium counterfactuals, not causal '
             'evaluations of actual tuition-free programs.',
             'Average gains can conceal losses for particular initial-endowment groups.'],
  'context': ['“Intermittent” includes delayed entry after high school, stopout (temporary exit) and '
              're-enrollment, not only dropout.',
              'Initial conditions at age 18 are a human capital proxy (AFQT score) and a wealth proxy '
              '(average family income at 17–19), fed into the model as an empirical joint distribution '
              'rather than a fitted normal.',
              'The paper was circulated earlier under the title “Best Time for College? A Tale of Two '
              'Endowments”.'],
  'data': 'NLSY79 (1979–2016) for life-cycle enrollment, completion and initial conditions; NLSY97 and '
          'CPS ASEC synthetic cohorts for robustness; detrended CPS wages 1992–2016 for calibration.',
  'method': 'Overlapping-generations life-cycle model with incomplete markets in general equilibrium '
            '(Huggett, Ventura and Yaron 2011 lineage). Each year individuals choose full-time work, '
            'part-time work with part-time school, full-time school, or non-employment; human capital '
            'accumulates on the job or in college with a sheepskin effect; welfare measured as '
            'consumption equivalence (Mukoyama 2010). Model earnings dynamics match Guvenen’s RIP and '
            'HIP estimates.',
  'whats_new': 'Evaluates the welfare value of access to college at each age and separates the '
               'investment and risk-reduction roles of college over the life cycle.',
  'audiences': ['Quantitative macroeconomists and macro-labor researchers',
                'Economists of education studying nontraditional students, stopout and adult completion',
                'Public finance researchers on tuition subsidies and tax incentives',
                'Higher-education policy analysts and journalists covering adult learners and '
                'free-college programs'],
  'related': [('Huggett, M., G. Ventura and A. Yaron (2011). Sources of lifetime inequality. American '
               'Economic Review 101(7): 2923–2954.',
               None),
              ('Castex, G. (2017). College risk and return. Review of Economic Dynamics 26: 91–112.',
               None),
              ('Abbott, B., G. Gallipoli, C. Meghir and G. L. Violante (2019). Education policy and '
               'intergenerational transfers in equilibrium. Journal of Political Economy 127(6): '
               '2569–2624.',
               None),
              ('Matsuda, K. (2020). Optimal timing of college subsidies: enrollment, graduation, and '
               'the skill premium. European Economic Review 129: 103549.',
               None),
              ('Athreya, K. and J. Eberly (2021). Risk, the college premium, and aggregate human '
               'capital investment. American Economic Journal: Macroeconomics 13(2): 168–213.',
               None),
              ('Johnson, M. T. (2013). Borrowing constraints, college enrollment, and delayed entry. '
               'Journal of Labor Economics 31(4): 669–725.',
               None),
              ('Arcidiacono, P., E. Aucejo, A. Maurel and T. Ransom (2025). College attrition and the '
               'dynamics of information revelation. Journal of Political Economy 133(1): 53–110.',
               None),
              ('Yang, G. and B. Casner (2021). How much does schooling disutility matter? Research in '
               'Economics 75(1): 87–95.',
               '10.1016/j.rie.2020.11.004')],
  'versions': [('Published article (Elsevier)', 'https://doi.org/10.1016/j.jedc.2025.105219'),
               ("Published PDF in the author's repository",
                'https://raw.githubusercontent.com/yangguanyi/Published/main/2025_JEDC_Yang.pdf'),
               ('Working paper version (PDF)',
                'https://github.com/yangguanyi/Working-papers/raw/master/College_timing_endowment.pdf'),
               ('RePEc listing', 'https://ideas.repec.org/f/pya376.html')],
  'questions': [('Why can returning to college help households manage risk?',
                 'In the model, people can use college after unfavorable labor-market outcomes, while '
                 'saving and borrowing also help them adjust. The value of that flexibility depends on '
                 'age, initial resources and borrowing constraints; it is not an individual '
                 'recommendation to enroll.'),
                ('What does the tuition-free counterfactual measure?',
                 'It compares long-run stationary equilibria in the calibrated model. Free tuition '
                 'increases degree attainment and consumption-equivalent welfare under lump-sum '
                 'financing. Those magnitudes are conditional on the model and financing assumptions, '
                 'rather than estimates from an implemented program.'),
                ('Does the student tax exemption benefit every group?',
                 'No. Average consumption-equivalent welfare rises by 1.62 percent, but the lowest '
                 'initial-human-capital group loses 2.3 percent after taxes and equilibrium prices '
                 'adjust. Changes in enrollment and welfare need to be distinguished (Tables 11 and '
                 '12).')],
  'funding': None,
  'short_summary': 'A life-cycle model measures how the option to delay or return to college helps '
                   'households invest in skills and respond to labor-market risk.',
  'reviewed_on': '2026-11-09',
  'pdf_path': 'papers/intermittent-college-enrollment/paper.pdf',
  'pdf_label': 'Read published paper (PDF)',
  'version_note': 'Summary based on the published article. The download is a smaller PDF with the same '
                  'text and research figures. The original publisher PDF is also linked below.',
  'publication_date': '2025-12',
  'volume': '181',
  'article_number': '105219',
  'online_date': '2025-11-21'},
 {'slug': 'informality-unemployment-small-open-economies',
  'kind': 'article',
  'theme': 'emerging-markets',
  'title': 'Unemployment Dynamics and Informality in Small Open Economies',
  'authors': [('Jaroslav Horvath', 'University of New Hampshire'), ('Guanyi Yang', 'Colorado College')],
  'year': 2022,
  'venue': 'European Economic Review',
  'venue_detail': 'Vol. 141, 103949',
  'doi': '10.1016/j.euroecorev.2021.103949',
  'jel': ['E26', 'F44', 'J64'],
  'keywords': ['informal economy', 'labor market frictions', 'emerging markets', 'business cycles'],
  'one_liner': 'Across 28 small open economies, unemployment fluctuates less relative to output in '
               'emerging markets than in advanced economies. A model calibrated to Mexico explains how '
               'informal employment absorbs labor reallocation, reducing unemployment fluctuations '
               'while amplifying changes in formal activity.',
  'abstract': 'Despite the typically more pronounced aggregate fluctuations in emerging market '
              'economies (EMEs), this paper documents that EMEs exhibit lower relative volatility and '
              'countercyclicality of the unemployment rate than small open advanced economies. We link '
              'these differences to the larger informal economy in EMEs. We build a small open economy '
              'model that combines a formal sector featuring labor search frictions with a frictionless '
              'informal sector. A larger informal sector amplifies the impact of productivity and '
              'interest rate shocks on formal output, consumption, and employment, while dampening '
              'their impact on unemployment. Varying the degree of informality explains a significant '
              'fraction of differences in unemployment dynamics across small open economies.',
  'findings': ['Unemployment volatility relative to output averages 4.63 in 14 emerging economies and '
               '7.74 in 14 small open advanced economies (p < 0.001). Its correlation with output '
               'averages -0.47 and -0.62, respectively (p = 0.047). The quarterly sample spans '
               '1980Q1-2018Q2, with different available periods across countries.',
               'Informality averages 30.8 percent of GDP in the emerging group vs 16.4 percent in the '
               'advanced group (Schneider et al. 2010); across countries, both relative unemployment '
               'volatility and countercyclicality fall as informality rises (p = 0.008 and 0.007).',
               'Calibrated to Mexico, the model reproduces relative unemployment volatility of 3.95 '
               '(data 3.89) and a correlation of −0.49 (data −0.35), along with consumption more '
               'volatile than output and a countercyclical trade balance.',
               'Varying the informal employment share from 0.1 to 0.5 moves relative unemployment '
               'volatility from 5.82 to 2.78 and the correlation from −0.68 to −0.23, tracing the '
               'cross-country pattern.',
               'Counting 52 percent of informal output in measured GDP lowers output volatility from '
               '3.24 to 2.58 and raises unemployment volatility relative to output from 3.95 to 4.97. '
               'Unemployment itself is unchanged in this measurement experiment.'],
  'limits': ['Cross-country facts cover 14 advanced and 14 emerging small open economies with '
             'sufficiently long quarterly data.',
             'The model is calibrated to Mexico and abstracts from the out-of-labor-force margin; '
             'informal production is modeled as firms facing audit risk, not self-employment.',
             'Sector-specific productivity shocks are assumed symmetric and uncorrelated, a '
             'conservative choice given the lack of data on informal productivity.',
             'The cross-country relationships and model counterfactuals do not establish the causal '
             'welfare effect of an informality-reduction policy.'],
  'context': ['Informality in the model is the informal share of total employment (0.3 for Mexico); the '
              'cross-country figures use the Schneider et al. (2010) share of GDP. The two are '
              'different measures.',
              'Informal workers search on the job for formal jobs, which is what gives the informal '
              'sector its buffering role.'],
  'data': 'An unbalanced quarterly panel of 28 small open economies from IMF International Financial '
          'Statistics, spanning 1980Q1 to 2018Q2 with different country windows; Schneider, Buehn and '
          'Montenegro (2010) informal-output estimates; Mexican labor-market flows from ENEU/ENOE via '
          'Leyva and Urrutia (2020); EMBI spreads.',
  'method': 'Small open economy real business cycle model with a formal sector subject to '
            'search-and-matching frictions and Nash bargaining, a frictionless informal sector with '
            'audit probability and fines, CES aggregation of formal and informal consumption, '
            'debt-elastic interest rate; log-linearized and calibrated to Mexico; shocks to formal and '
            'informal productivity and to the country interest rate.',
  'whats_new': 'A new cross-country fact about unemployment in emerging markets and a mechanism, the '
               'size and mismeasurement of the informal sector, that explains it within a standard '
               'search framework.',
  'audiences': ['International and development macroeconomists working on emerging-market business '
                'cycles',
                'Labor-search modelers working on open economies and dual labor markets',
                'Researchers on the informal sector and shadow economy',
                'Central bank and IMF/World Bank economists covering Mexico and Latin America'],
  'related': [('Fernández, A. and F. Meza (2015). Informal employment and business cycles in emerging '
               'economies: the case of Mexico. Review of Economic Dynamics 18(2): 381–405.',
               None),
              ('Leyva, G. and C. Urrutia (2020). Informality, labor regulation, and the business cycle. '
               'Journal of International Economics 126: 103340.',
               None),
              ('Restrepo-Echavarria, P. (2014). Macroeconomic volatility: the role of the informal '
               'economy. European Economic Review 70: 454–469.',
               None),
              ('Finkelstein Shapiro, A. (2018). Labor force participation, interest rate shocks, and '
               'unemployment dynamics in emerging economies. Journal of Development Economics 133: '
               '346–374.',
               None),
              ('Boz, E., C. B. Durdu and N. Li (2015). Emerging market business cycles: the role of '
               'labor market frictions. Journal of Money, Credit and Banking 47(1): 31–72.',
               None),
              ('Neumeyer, P. A. and F. Perri (2005). Business cycles in emerging economies: the role of '
               'interest rates. Journal of Monetary Economics 52(2): 345–380.',
               None),
              ('Aguiar, M. and G. Gopinath (2007). Emerging market business cycles: the cycle is the '
               'trend. Journal of Political Economy 115(1): 69–102.',
               None)],
  'versions': [('Published article (Elsevier)', 'https://doi.org/10.1016/j.euroecorev.2021.103949'),
               ("Published PDF in the author's repository",
                'https://raw.githubusercontent.com/yangguanyi/Published/main/2022_EER_Horvath_Yang.pdf'),
               ('RePEc listing', 'https://ideas.repec.org/f/pya376.html')],
  'questions': [('How can informal work buffer unemployment fluctuations?',
                 'In the calibrated model, expanding formal firms recruit from informal work as well as '
                 'unemployment. This additional adjustment margin makes unemployment less volatile '
                 'relative to formal output, providing a mechanism consistent with the cross-country '
                 'evidence.'),
                ('Does lower unemployment volatility imply that informality improves welfare?',
                 'The paper studies business-cycle dynamics and measurement. It does not estimate the '
                 'causal welfare effect of formalization or show that workers prefer informal jobs.')],
  'funding': None,
  'short_summary': 'Cross-country evidence and a model of Mexico examine how informal employment '
                   'buffers unemployment fluctuations.',
  'reviewed_on': '2026-11-09',
  'pdf_path': 'papers/informality-unemployment-small-open-economies/paper.pdf',
  'pdf_label': 'Read published paper (PDF)',
  'version_note': 'Summary based on the published article linked here. Earlier working-paper versions '
                  'are listed separately below.',
  'publication_date': '2022-01',
  'volume': '141',
  'article_number': '103949',
  'online_date': '2021-10-26'},
 {'slug': 'sibling-spillovers-rural-china',
  'kind': 'article',
  'theme': 'china-education',
  'title': 'Sibling Spillovers in Rural China: A Story of Sisters',
  'authors': [('Cynthia Bansak', 'St. Lawrence University'),
              ('Xuan Jiang', 'Jinan University'),
              ('Guanyi Yang', 'Colorado College')],
  'year': 2022,
  'venue': 'China Economic Review',
  'venue_detail': 'Vol. 76, 101873',
  'doi': '10.1016/j.chieco.2022.101873',
  'jel': ['I21', 'I24', 'J13', 'J16', 'O15'],
  'jel_note': 'Topic classifications added for this website; the published article prints E24, C68 and '
              'J30.',
  'keywords': ['human capital',
               'peer effect',
               'sibling spillover',
               'rural China',
               'sisters',
               'girls',
               'school enrollment',
               'intra-household allocation',
               'intra-household externality'],
  'one_liner': 'Using school-entry eligibility in rural China, we estimate that an additional year of a '
               "younger sibling's schooling raises the older child's Chinese score by about 1.4 points "
               'on a 100-point scale. The strongest evidence comes from younger sisters; '
               'mathematics-score effects are not statistically significant.',
  'abstract': 'We study sibling spillover effects on the school performance of the elder sibling from '
              'the younger sibling using data on multi-children households in rural China. Using a '
              'cumulative measure of expected lawful years in school as an instrumental variable, we '
              'find a significant increase in school test scores for Chinese language of elder siblings '
              'for every year of schooling of the younger sibling. The strongest spillover effects '
              'occur when the younger sibling is a girl. Such increases in test scores come from a more '
              'intense academic atmosphere within a household when both children enroll in school and '
              'are not attributed to differential parental education investments or time inputs. Our '
              'findings suggest that policies promoting girls’ education, pre-elementary school age '
              'education programs, and after school public resources can have multiplier effects '
              'through sibling spillovers.',
  'findings': ["The preferred IV estimate is 1.420 additional points on the older sibling's Chinese "
               'score per year of younger-sibling schooling, with a standard error of 0.663. It is '
               'significant at 5 percent and uses 289 observations. The mathematics estimate is '
               'positive but not statistically significant (Table 2).',
               'The younger-sister estimate is 2.256 points, significant at 5 percent, in a sample of '
               '103. The younger-brother estimate is 1.251 points and is not statistically significant. '
               'These separate significance results do not establish a significant difference between '
               'the two groups (Table 4).',
               'Estimates vary across the younger-sibling age windows considered. Restricting ages to 5 '
               'to 8 gives 4.930 points with 151 observations, so the larger estimate should be read '
               'alongside its smaller sample (Table 3).',
               "The estimated spillover is about 3.1 points smaller when the older child's school is "
               'farther than the median distance from home; this interaction is significant at 10 '
               'percent. This is consistent with a household learning mechanism, rather than direct '
               'evidence on study time (Table 5).',
               'The authors find no statistically detectable schooling-related change in spending on '
               'the older child or in parental presence, an imperfect proxy for parental time and '
               'attention (Table A3).',
               'The first-stage Kleibergen-Paap F statistic is 91.29 in the preferred specification '
               'with 289 observations. The baseline specification with 346 observations has an F '
               'statistic of 144.66 (Tables 2 and A2).'],
  'limits': ['The baseline sample has 346 older children from rural two-child households in nine '
             'provinces; the preferred specification uses 289. The younger-sister subgroup contains 103 '
             'observations.',
             'Exam scores are self-reported and rescaled to a 100-point scale. The relevant scores come '
             'from one survey wave, and only Chinese-score effects are statistically significant.',
             'Identification relies on school-entry eligibility affecting older-sibling scores through '
             "the younger child's schooling. The home-environment mechanism is inferred from distance "
             'and ancillary regressions, not observed study time.',
             'The paper does not evaluate a specific preschool or after-school intervention, long-term '
             'attainment, or earnings.'],
  'context': ['The direction of the spillover is younger to elder, the reverse of most of the '
              'sibling-spillover literature.',
              'The instrument is lawful years of schooling implied by China’s Compulsory Education Law '
              'cutoff: children must turn six by August 31 to enroll that September.',
              'Earlier versions circulated as “Sibling Spillover in Rural China: A Story of Sisters and '
              'Daughters” (IZA Discussion Paper 13127; EdWorkingPaper 21-465).'],
  'data': 'RUMiC Rural Household Survey, 2008 and 2009 waves, in nine Chinese provinces. The baseline '
          'sample is 346 older children in two-child rural households whose younger sibling was aged 3 '
          'to 9 in 2008. Chinese and mathematics examination scores are rescaled to 100 points; the '
          'preferred regression uses 289 observations.',
  'method': 'Two-stage least squares instruments actual years of younger-sibling schooling with '
            'cumulative lawful schooling implied by the sixth-birthday school-entry cutoff. Regressions '
            'include child, parent, household and geographic controls, with standard errors clustered '
            'by city. This is an IV design using school-entry eligibility, not a conventional local '
            'regression discontinuity design.',
  'whats_new': 'Studies education spillovers from younger siblings to older siblings in rural China, '
               'with evidence that is strongest for younger sisters and consistent with changes in the '
               'household learning environment.',
  'audiences': ['Economists of education and family economics',
                'Development economists working on China, gender and schooling',
                'Researchers on peer effects and intra-household externalities',
                'Girls’-education policy analysts'],
  'related': [('Black, S. E., S. Breining, D. N. Figlio, J. Guryan, K. Karbownik, H. S. Nielsen, J. '
               'Roth and M. Simonsen (2021). Sibling spillovers. Economic Journal 131(633): 101–128 '
               '(online 2020).',
               None),
              ('Qureshi, J. A. (2018). Siblings, teachers, and spillovers on academic achievement. '
               'Journal of Human Resources 53(1): 272–297.',
               None),
              ('Joensen, J. S. and H. S. Nielsen (2018). Spillovers in education choice. Journal of '
               'Public Economics 157: 158–183.',
               None),
              ('Biavaschi, C., C. Giulietti and K. F. Zimmermann (2015). Sibling influence on the human '
               'capital of the left-behind. Journal of Human Capital 9(4): 403–438.',
               None),
              ('Jakiela, P., O. Ozier, L. Fernald and H. Knauer (2020). Big sisters. World Bank Policy '
               'Research Working Paper 9454.',
               None),
              ('Yang, G. and C. Bansak (2020). Does wealth matter? An assessment of China’s rural-urban '
               'migration on the education of left-behind children. China Economic Review 59: 101365.',
               '10.1016/j.chieco.2019.101365')],
  'versions': [('Published article (Elsevier)', 'https://doi.org/10.1016/j.chieco.2022.101873'),
               ("Published PDF in the author's repository",
                'https://raw.githubusercontent.com/yangguanyi/Published/main/2022_CER_Bansak_Jiang_Yang.pdf'),
               ('Working paper version, September 2022 (PDF)',
                'https://github.com/yangguanyi/Working-papers/raw/master/sib_spillover_China.pdf'),
               ('EdWorkingPaper 21-465 (Annenberg Institute, Brown University)',
                'https://www.edworkingpapers.com/ai21-465'),
               ('IZA Discussion Paper 13127',
                'https://www.iza.org/publications/dp/13127/sibling-spillover-in-rural-china-a-story-of-sisters-and-daughters'),
               ('RePEc listing', 'https://ideas.repec.org/f/pya376.html')],
  'questions': [["Can a younger sibling's schooling improve an older sibling's performance?",
                 'In this rural Chinese sample, the preferred IV estimate is about 1.4 additional '
                 'Chinese-score points on a 100-point scale per year of younger-sibling schooling. '
                 'Mathematics effects are not statistically significant, and the finding depends on the '
                 "school-entry instrument's assumptions."],
                ['What does the paper find about younger sisters?',
                 'The younger-sister estimate is about 2.26 Chinese-score points and is statistically '
                 'significant; the younger-brother estimate is imprecise. The authors interpret '
                 'distance and household-investment results as consistent with a more academic home '
                 'environment, but do not observe study time directly.']],
  'funding': None,
  'short_summary': 'School-entry eligibility identifies education spillovers from younger to older '
                   'siblings in rural China, with the strongest evidence among younger sisters.',
  'reviewed_on': '2026-11-09',
  'pdf_path': 'papers/sibling-spillovers-rural-china/paper.pdf',
  'pdf_label': 'Read published paper (PDF)',
  'version_note': 'Summary based on the published article linked here. Earlier working-paper versions '
                  'are listed separately below.',
  'publication_date': '2022-12',
  'volume': '76',
  'article_number': '101873',
  'online_date': '2022-10-13'},
 {'slug': 'global-financial-risk-equity-returns-emerging-markets',
  'kind': 'article',
  'theme': 'emerging-markets',
  'title': 'Global Financial Risk, Equity Returns and Economic Activity in Emerging Countries',
  'authors': [('Jaroslav Horvath', 'University of New Hampshire'), ('Guanyi Yang', 'Colorado College')],
  'year': 2024,
  'venue': 'Oxford Bulletin of Economics and Statistics',
  'venue_detail': 'Vol. 86, No. 3, pp. 672–689',
  'doi': '10.1111/obes.12595',
  'jel': ['E32', 'E37', 'F34', 'F37', 'G15'],
  'keywords': ['global financial risk',
               'VIX',
               'emerging market economies',
               'equity returns',
               'country spreads',
               'capital flows',
               'panel SVAR',
               'global financial cycle'],
  'one_liner': 'A panel SVAR for 12 emerging economies links global financial risk to output and '
               'investment through capital flows, equity returns and borrowing spreads. Removing equity '
               "returns' response to global risk in a model counterfactual reduces the risk share of "
               'output-growth forecast-error variance from about 10 percent to 2 percent.',
  'abstract': 'International financial integration exposes countries to external shocks. This paper '
              'identifies the impact and transmission of global financial risk (GFR) shocks to emerging '
              'market economies (EMEs). Heightened GFR significantly raises EME borrowing costs and '
              'lowers equity returns, reducing domestic economic activity. We document a novel '
              'transmission channel of GFR shocks to EMEs via international capital flows. Countries '
              'experiencing larger capital inflows are more affected by GFR fluctuations. Exploring the '
              'transmission through capital flows, GFR shocks affect EMEs mainly through their effect '
              'on equity returns, instead of country spreads. We show that equity returns contain more '
              'information about EME macroeconomic fluctuations than sovereign and corporate bond '
              'spreads.',
  'findings': ['A one-standard-deviation adverse global-risk innovation reduces annual output growth by '
               'over 0.4 percentage points and annual investment growth by over 0.8 points at the '
               'trough, about five quarters after the shock (Figure 2).',
               'In the baseline 20-quarter forecast-error variance decomposition, global risk '
               'contributes about 10 percent of output-growth variance, close to 5 percent of '
               'investment-growth variance, more than 7 percent of country-spread variance and over 15 '
               'percent of equity-return variance (Figure 3).',
               'In countries with above-median average net US capital inflows relative to GDP, global '
               'risk accounts for over 15 percent of output-growth forecast-error variance, roughly '
               'twice the share in the lower-exposure group (Figure 4).',
               'Removing the direct response of equity returns to global risk reduces its output-growth '
               'variance share from about 10 to 2 percent and its investment-growth share from 5 to '
               'near zero. Removing the country-spread response leaves these shares almost unchanged '
               '(Figures 5 and 6).',
               'Equity-return innovations account for about a quarter of output- and investment-growth '
               'forecast-error variance in this specification. Sovereign-spread innovations contribute '
               'little, and equity innovations also explain more than corporate-spread innovations in '
               'the reduced sample (Figures 7 and 8).'],
  'limits': ['Twelve emerging economies, 1999Q1–2019Q4 (Indonesia from 2004Q2, Thailand to 2006Q1); the '
             'sample ends before the pandemic.',
             'Identification is a recursive panel SVAR with global financial risk ordered as an '
             'exogenous block and equity returns ordered last; capital flows are measured vis-à-vis the '
             'United States (TIC data), with a robustness check using global flows.',
             'The collateral-constraint model (Mendoza and Smith 2006) is used to interpret the '
             'mechanism, not estimated.'],
  'context': ['The published baseline uses the VIX as the global-risk proxy; a robustness exercise uses '
              'the US Baa credit spread.',
              'Country spreads are J.P. Morgan EMBIG; corporate spreads are the EFI of Caballero, '
              'Fernández and Park (2019) and J.P. Morgan’s CEMBI.'],
  'data': 'IMF International Financial Statistics (output, investment, trade balance); J.P. Morgan '
          'EMBIG spreads via World Bank GEM; Global Financial Data stock indexes; U.S. Treasury TIC '
          'capital flows; VIX and Baa spread from FRED. Quarterly, 1999Q1–2019Q4.',
  'method': 'Panel structural VAR (least-squares dummy variable estimation, one lag, recursive '
            'identification) with output, investment, trade balance, global financial risk, capital '
            'flows, country spread and equity returns; impulse responses, variance decompositions and '
            'counterfactuals that mute specific transmission channels.',
  'whats_new': 'Compares equity and borrowing-spread transmission channels in emerging-market business '
               'cycles, including international capital flows in the estimated panel SVAR.',
  'audiences': ['International macroeconomists and finance researchers on emerging-market business '
                'cycles',
                'Economists working on the global financial cycle and VIX spillovers',
                'Emerging-market central bank research departments',
                'Asset managers and analysts following EM equities and capital flows'],
  'related': [('Akinci, Ö. (2013). Global financial conditions, country spreads and macroeconomic '
               'fluctuations in emerging countries. Journal of International Economics 91(2): 358–371.',
               None),
              ('Caballero, J., A. Fernández and J. Park (2019). On corporate borrowing, credit spreads '
               'and economic activity in emerging economies: an empirical investigation. Journal of '
               'International Economics 118: 160–178.',
               None),
              ('Epstein, B., A. F. Shapiro and A. G. Gómez (2019). Global financial risk, aggregate '
               'fluctuations, and unemployment dynamics. Journal of International Economics 118: '
               '351–418.',
               None),
              ('Bhattarai, S., A. Chatterjee and W. Y. Park (2020). Global spillover effects of US '
               'uncertainty. Journal of Monetary Economics 114: 71–89.',
               None),
              ('Uribe, M. and V. Z. Yue (2006). Country spreads and emerging countries: who drives '
               'whom? Journal of International Economics 69(1): 6–36.',
               None),
              ('Mendoza, E. G. and K. A. Smith (2006). Quantitative implications of a debt-deflation '
               'theory of sudden stops and asset prices. Journal of International Economics 70(1): '
               '82–114.',
               None),
              ('Rey, H. (2015). Dilemma not trilemma: the global financial cycle and monetary policy '
               'independence. NBER Working Paper 21162.',
               None)],
  'versions': [('Published article (Wiley)', 'https://doi.org/10.1111/obes.12595'),
               ("Published PDF in the author's repository",
                'https://raw.githubusercontent.com/yangguanyi/Published/main/2024_OBES_Horvath_Yang.pdf'),
               ('Working paper version, December 2023 (PDF)',
                'https://github.com/yangguanyi/Working-papers/raw/master/GFR_and_equity_returns.pdf'),
               ('RePEc article record', 'https://ideas.repec.org/a/bla/obuest/v86y2024i3p672-689.html')],
  'questions': [('How do global financial-risk shocks reach emerging economies?',
                 'The panel SVAR estimates capital outflows, lower equity returns, higher borrowing '
                 'spreads and weaker output and investment growth after an adverse global-risk '
                 'innovation. Their interpretation depends on the recursive identification and '
                 'small-open-economy assumptions.'),
                ('What does the equity-channel counterfactual show?',
                 "Within the estimated model, removing equity returns' direct response to global risk "
                 'sharply reduces the share of output-growth forecast-error variance attributed to '
                 'global risk. The corresponding sovereign-spread counterfactual changes little. This '
                 'is a channel decomposition, not an observed policy experiment.')],
  'funding': None,
  'short_summary': 'A panel SVAR compares equity markets and borrowing spreads as channels for global '
                   'financial-risk shocks in emerging economies.',
  'reviewed_on': '2026-11-09',
  'pdf_path': 'papers/global-financial-risk-equity-returns-emerging-markets/paper.pdf',
  'pdf_label': 'Read published paper (PDF)',
  'version_note': 'Summary based on the published article linked here. Earlier working-paper versions '
                  'are listed separately below.',
  'publication_date': '2024-06',
  'volume': '86',
  'issue': '3',
  'first_page': '672',
  'last_page': '689',
  'online_date': '2024-01-05'},
 {'slug': 'left-behind-children-parental-migration-wealth',
  'kind': 'article',
  'theme': 'china-education',
  'title': 'Does Wealth Matter? An Assessment of China’s Rural-Urban Migration on the Education of '
           'Left-Behind Children',
  'authors': [('Guanyi Yang', 'Colorado College (St. Lawrence University at publication)'),
              ('Cynthia Bansak', 'St. Lawrence University')],
  'year': 2020,
  'venue': 'China Economic Review',
  'venue_detail': 'Vol. 59, 101365',
  'doi': '10.1016/j.chieco.2019.101365',
  'jel': ['I25', 'J13', 'O15', 'R23'],
  'jel_note': 'The published article does not print JEL codes; the codes here were added for this page.',
  'keywords': ['wealth heterogeneity',
               'human capital',
               'China',
               'rural-urban migration',
               'absenteeism',
               'parental inputs',
               'left-behind children'],
  'one_liner': 'Parental migration brings more income but less parental time. This paper studies how '
               'that tradeoff varies with family wealth, using a household model and rural Chinese data '
               'on whether children attend the grade appropriate for their age. It examines whether '
               'additional resources can partly offset parental absence.',
  'abstract': 'This paper decomposes the impact of parental migration on the education of children left '
              'behind. In particular, we examine whether children are enrolled in school on a timely '
              'basis according to their age when their parents are away. We found both theoretical and '
              'empirical evidence to support that parental migration generates a strong positive impact '
              'on timely enrollment if a child is from a less wealthy background. However, the effect '
              'decreases with family wealth, and reverses after reaching a threshold; we find this '
              'point using family house size as our proxy and the turning point occurs at a moderate '
              'size of approximately 148 square meters. In addition, we find a compensating effect that '
              'migrants tend to spend more on a child’s education investment to offset for the loss of '
              'parental time care. Lastly, we found the overall impact of parental migration is '
              'negative on the timely enrollment of child. Thus, with the important heterogeneities '
              'attributed to wealth, our results suggest that the left behind children of more affluent '
              'parents may be pushed into worse human capital outcomes; given the rapid development of '
              'China, it may be the case that the current cohort of left behind children is less likely '
              'to be enrolled in school than earlier cohorts.',
  'findings': ['The household model explains why initial wealth can change the balance between '
               'additional financial resources and lost parental time when a parent migrates (Section '
               '3).',
               'The empirical model interacts parental migration with house size, a proxy for household '
               'wealth. It studies heterogeneous effects rather than one constant migration effect for '
               'every family (Equation 1; Tables 2 and 3).',
               'The migration-by-house-size coefficient is negative in the lower-wealth subsample. '
               'Estimates for wealthier households are less precise, and the overall migration result '
               'is sensitive to the controls included (Tables 2, 3 and 6).',
               'The authors examine school transportation as an indirect indicator of compensating '
               'resource investment. Bus-taking is associated with higher education spending, but these '
               'data do not identify school quality or a causal spending mechanism (Tables 4 and 5).'],
  'limits': ['House size is a proxy for wealth. The outcome is age-appropriate school enrollment, not '
             'examination scores, completed schooling or adult earnings.',
             'The 148-square-meter split defines subsamples in this analysis; it should not be read as '
             'a universal threshold where migration necessarily changes from beneficial to harmful.',
             'Identification relies on migration-network and provincial-wage instruments for migration '
             'and parental-height instruments for house size. Exclusion restrictions are assumptions, '
             'and several fully controlled first-stage diagnostics are weak.',
             'Estimates for wealthier households are imprecise. School transportation is an indirect '
             'resource-investment proxy, and its relationship to school quality is not causally '
             'established.'],
  'context': ['The theory models child human capital as a product of parental time and financial '
              'resources. Migration reduces available parental time but can increase the resources that '
              'a household invests in a child.',
              "The paper's rural Chinese setting concerns children who remain behind while a parent "
              'migrates. It does not estimate school outcomes for children who accompany parents to '
              'cities.'],
  'data': 'China Health and Nutrition Survey waves from 1997, 2000, 2004, 2006, 2009, 2011 and 2015. '
          'The underlying rural sample contains 4,502 children, 2,826 households, 175 communities and '
          '14,298 child-year observations in 12 provinces. Enrollment regressions concern children aged '
          '6 to 18 and use smaller samples because of missing data and age restrictions.',
  'method': 'A two-period household model of parental time and financial investment, followed by '
            'instrumental-variable regressions of age-appropriate enrollment on migration, house size '
            'and their interaction. Instruments use historical community migration networks, provincial '
            'wage changes and parental height. Regressions compare wealth subsamples and cluster '
            'standard errors by household.',
  'whats_new': 'Connects a model of parental time and financial resources with evidence on how '
               'household wealth can shape the schooling consequences of rural-to-urban migration.',
  'audiences': ['Development economists working on China, migration and the hukou system',
                'Economists of education and child development',
                'Family economists studying parental time versus money inputs',
                'Policy analysts at UNICEF, the World Bank and Chinese agencies working on left-behind '
                'children'],
  'related': [('Mu, R. and A. de Brauw (2015). Migration and young child nutrition: evidence from rural '
               'China. Journal of Population Economics 28(3): 631–657.',
               None),
              ('Zhou, M., R. Murphy and R. Tao (2014). Effects of parents’ migration on the education '
               'of children left behind in rural China. Population and Development Review 40(2): '
               '273–292.',
               None),
              ('Wang, X., Y. Bai, L. Zhang and S. Rozelle (2017). Migration, schooling choice, and '
               'student outcomes in China. Population and Development Review 43(4): 625–643.',
               None),
              ('Hu, F. (2012). Migration, remittances, and children’s high school attendance: the case '
               'of rural China. International Journal of Educational Development 32(3): 401–411.',
               None),
              ('Démurger, S. and H. Xu (2015). Left-behind children and return migration in China. IZA '
               'Journal of Migration 4: 10.',
               None),
              ('Del Boca, D., C. Flinn and M. Wiswall (2014). Household choices and child development. '
               'Review of Economic Studies 81(1): 137–185.',
               None)],
  'versions': [('Published article (Elsevier)', 'https://doi.org/10.1016/j.chieco.2019.101365'),
               ("Published PDF in the author's repository",
                'https://raw.githubusercontent.com/yangguanyi/Published/main/2020_CER_Yang_Bansak.pdf'),
               ('RePEc listing', 'https://ideas.repec.org/f/pya376.html')],
  'questions': [["Why might parental migration affect children's schooling differently across families?",
                 'Migration can add financial resources while reducing parental time. The model shows '
                 'why the balance can depend on initial household wealth, and the empirical analysis '
                 'examines that heterogeneity using house size as a wealth proxy.'],
                ['What education outcome does the paper measure?',
                 'It measures whether rural children are enrolled in the grade appropriate for their '
                 'age. It does not measure examination performance or the experience of children who '
                 'migrate with their parents.'],
                ['Does the study identify one house-size threshold that applies to every family?',
                 'No. It compares subsamples divided at 148 square meters in these data. The results '
                 'depend on the specification and identifying assumptions, and estimates for wealthier '
                 'households are imprecise.']],
  'funding': None,
  'short_summary': 'A household model and rural Chinese data examine how wealth shapes the tradeoff '
                   "between migrant parents' time and financial resources.",
  'reviewed_on': '2026-11-09',
  'pdf_path': 'papers/left-behind-children-parental-migration-wealth/paper.pdf',
  'pdf_label': 'Read published paper (PDF)',
  'version_note': 'Summary based on the published article linked here. Earlier working-paper versions '
                  'are listed separately below.',
  'publication_date': '2020-02',
  'volume': '59',
  'article_number': '101365',
  'online_date': '2019-11-05'},
 {'slug': 'temporary-employment-us-welfare',
  'kind': 'article',
  'theme': 'college-lifecycle',
  'title': 'Welfare Under Friction and Uncertainty: General Equilibrium Evaluation of Temporary '
           'Employment in the U.S.',
  'authors': [('Guanyi Yang', 'Colorado College (St. Lawrence University at publication)')],
  'year': 2018,
  'venue': 'Research in Economics',
  'venue_detail': 'Vol. 72, No. 3, pp. 404–413',
  'doi': '10.1016/j.rie.2018.07.005',
  'jel': ['E24', 'C68', 'J30'],
  'keywords': ['labor market misallocation',
               'temporary employment',
               'firing costs',
               'idiosyncratic uncertainty',
               'general equilibrium',
               'heterogeneous agents'],
  'one_liner': 'In a U.S.-calibrated model, temporary contracts help firms absorb productivity risk and '
               'reduce the aggregate welfare losses caused by firing costs. They only partly offset '
               'those losses, because firms substitute toward less productive temporary labor.',
  'abstract': 'Temporary contracts usually fall outside of employee protection litigation, thus they '
              'are often cheaper than permanent contracts and are offered on-demand by firms. In the '
              'last two decades, there has been a sharp growth in such contracts in the U.S. labor '
              'market. This paper investigates the welfare consequences of offering temporary contracts '
              'in the U.S., an environment with low employee protection litigation and high production '
              'risk for firms. Employee protection litigation creates firing rigidity in regular labor '
              'markets. Pairing firing rigidity with high production risk, firms reduce employment and '
              'output, which generates welfare loss. The inexpensive and flexible nature of temporary '
              'contracts offers firms a buffer strategy in making employment decisions under risk and '
              'navigating the firing rigidity of the regular labor sector, thereby reducing welfare '
              'loss. However, temporary contracts cannot fully compensate for the efficiency cost from '
              'rising firing rigidity and risk.',
  'findings': ['When firing costs rise to one year of wages, normalized net utility is 96.51 with '
               "temporary contracts and 95.26 without. Each regime's zero-firing-cost benchmark is "
               'normalized separately to 100; these are not consumption-equivalent percentages. (Table '
               '4).',
               'Doubling productivity-innovation variance, by raising its standard deviation from 0.259 '
               'to 0.3663, yields normalized net utility of 85.66 with temporary contracts and 83.81 '
               "without, relative to each regime's lower-risk baseline. (Table 5).",
               'Temporary contracts widen the inaction region for regular employment because firms can '
               'substitute toward less productive temporary labor when firing costs make regular-worker '
               'adjustment expensive.',
               'Temporary help accounted for 25.64 percent of job losses in the 2001 recession and '
               '54.99 percent of job gains in the recovery after the 2009 recession. Contributions '
               'differ across episodes. (Appendix A).'],
  'limits': ['Annual model period, so within-year temp turnover is not captured; no firm entry or exit; '
             'a representative household.',
             'Calibrated to the U.S. with a 2 percent temporary share and a 0.7 wage ratio; results are '
             'model-based welfare comparisons, not causal estimates.',
             'A representative household pools earnings and firm profits, so aggregate welfare results '
             'do not establish gains for temporary workers individually.',
             'Temporary-help industry employment is a proxy and does not cover all fixed-term, '
             'contingent, or gig work.'],
  'context': ['The model extends Hopenhayn and Rogerson (1993) with two labor inputs: regular labor '
              'subject to a firing cost and temporary labor hired period by period.',
              'The paper argues against treating temporary employment as equivalent to a firing-tax '
              'reduction, the interpretation in Aguirregabiria and Alonso-Borrego (2014) for Spain.'],
  'data': 'Longitudinal Business Database firm-size distribution 1977–2013; BLS Current Employment '
          'Statistics for temporary help services, 1972–2015; wage ratio and labor share targets.',
  'method': 'Dynamic general equilibrium model with heterogeneous firms facing AR(1) idiosyncratic '
            'productivity (Tauchen discretization), CES production in regular and temporary labor, a '
            'linear firing cost on regular labor, and a representative household with indivisible '
            'labor; calibrated to U.S. moments; counterfactuals vary firing costs and volatility with '
            'and without temporary contracts.',
  'whats_new': 'Brings the temporary-contract welfare question to the U.S. setting of low rigidity and '
               'high firm risk, with an endogenous temporary-employment share rather than an exogenous '
               'one.',
  'audiences': ['Labor macroeconomists working on employment protection, firm dynamics and '
                'misallocation',
                'Researchers on temporary help, fixed-term and contingent work',
                'Policy analysts on labor-market flexibility'],
  'related': [('Hopenhayn, H. and R. Rogerson (1993). Job turnover and policy evaluation: a general '
               'equilibrium analysis. Journal of Political Economy 101(5): 915–938.',
               None),
              ('Aguirregabiria, V. and C. Alonso-Borrego (2014). Labor contracts and flexibility: '
               'evidence from a labor market reform in Spain. Economic Inquiry 52(2): 930–957.',
               None),
              ('Autor, D. H. and S. N. Houseman (2010). Do temporary-help jobs improve labor market '
               'outcomes for low-skilled workers? Evidence from ‘Work First’. American Economic '
               'Journal: Applied Economics 2(3): 96–128.',
               None),
              ('Cahuc, P. and F. Postel-Vinay (2002). Temporary jobs, employment protection and labor '
               'market performance. Labour Economics 9(1): 63–91.',
               None),
              ('Comin, D. A. and T. Philippon (2005). The rise in firm-level volatility: causes and '
               'consequences. NBER Working Paper 11388; published in NBER Macroeconomics Annual 20 '
               '(2006): 167–228.',
               None)],
  'versions': [('Published article (Elsevier)', 'https://doi.org/10.1016/j.rie.2018.07.005'),
               ("Published PDF in the author's repository",
                'https://raw.githubusercontent.com/yangguanyi/Published/main/2018_RIE_Yang.pdf'),
               ('RePEc listing', 'https://ideas.repec.org/f/pya376.html')],
  'questions': [('How do temporary contracts change the aggregate cost of firing restrictions?',
                 'They let firms adjust employment around firing costs and partially cushion the '
                 'aggregate effects of productivity risk. The representative-household model measures '
                 'aggregate welfare and does not establish whether each temporary worker benefits.')],
  'funding': None,
  'short_summary': 'A model of heterogeneous firms measures how temporary contracts cushion the '
                   'aggregate costs of firing restrictions and productivity risk.',
  'reviewed_on': '2026-11-09',
  'pdf_path': 'papers/temporary-employment-us-welfare/paper.pdf',
  'pdf_label': 'Read published paper (PDF)',
  'version_note': 'Summary based on the published article linked here. Earlier working-paper versions '
                  'are listed separately below.',
  'publication_date': '2018-09',
  'volume': '72',
  'issue': '3',
  'first_page': '404',
  'last_page': '413',
  'online_date': '2018-07-24'},
 {'slug': 'social-norms-information-green-fee',
  'kind': 'article',
  'theme': 'behavior-public-goods',
  'title': 'How Much Versus Who: Which Social Norms Information Is More Effective?',
  'authors': [('Andrew Meyer', 'Marquette University'),
              ('Guanyi Yang', 'Colorado College (Ohio State University at publication)')],
  'year': 2016,
  'venue': 'Applied Economics',
  'venue_detail': 'Vol. 48, No. 5, pp. 389–401 (published online 11 September 2015)',
  'doi': '10.1080/00036846.2015.1080803',
  'jel': ['Q50', 'C90', 'H41', 'D03'],
  'keywords': ['social norms', 'stated preference', 'pro-environment behaviour', 'referendum'],
  'one_liner': 'In a randomized survey of 559 college students, information about high support for '
               'campus green fees raised the maximum fee students said they would approve by about $7 '
               'per semester. Information about fee amounts at other schools reduced it by about $8.50. '
               'The combined message had no statistically detectable effect.',
  'abstract': 'We conduct an experiment to investigate how different types of information about social '
              'norms affect individuals’ stated contributions to a specific pro-environment program, a '
              'student ‘green fee’, in the context of a referendum. Compared to students that receive '
              'no information about peer contributions, on average, students that receive information '
              'about the dollar value range of contributions at peer institutions contribute less while '
              'students that learn about the high percentage of students voting ‘yes’ on green fee '
              'programs at peer institutions contribute more. The results are economically significant '
              'as the absolute values of both effects represent approximately 25% of average '
              'contributions. These results suggest that information about participation rates can be '
              'more effective than information about dollar amounts in encouraging contributions to '
              'environmental initiatives. Of interest to stated preference researchers, we find that '
              'results do not change when controlling for self-selection into survey completion.',
  'findings': ["In the hypothetical referendum, the control group's mean maximum approved semester fee "
               'was $31.83. The fee-amount message reduced it to $23.33, a difference of $8.50; the '
               'high-participation message raised it to $38.94, a difference of $7.10 (Table 2).',
               'The combined message produced a mean of $32.71, which was not statistically different '
               'from the control mean. This does not establish that the two effects cancel exactly '
               '(Table 2).',
               'The share selecting zero fell from 15.6 percent in the control group to 7.1 percent '
               'with the high-participation message (Table 3).',
               'Interval-regression estimates were about -$8.09 for fee-amount information and +$7.25 '
               'for high-participation information. The latter was significant at 10 percent in this '
               'specification (Table 4).',
               'Selection models using administrative student data produced similar treatment estimates '
               "under the models' assumptions (Table 5)."],
  'limits': ['The study covers one Midwestern liberal arts university in October 2011, with a response '
             'rate of about 30 percent.',
             'The outcome is stated support in a hypothetical mandatory-fee referendum. The study does '
             'not observe actual payments, voluntary donations or an implemented campus vote.',
             'The participation treatment combines information about the number of schools with green '
             'fees and high yes-vote percentages. It does not isolate the effect of the number 85 '
             'percent or establish that participation information is always more effective.',
             'The design cannot distinguish conformity from reciprocity. Similar selection-adjusted '
             'estimates do not rule out every form of survey-selection bias.'],
  'context': ['Students were asked for the largest semester fee they would vote to approve if the fee '
              'became mandatory for all students. A payment card offered amounts from $0 to $100 in $5 '
              'increments.',
              'The fee-amount message reported true fees at peer institutions ranging from $1 per '
              'credit to $80 per year. The participation message reported programs at more than 70 '
              'schools and high approval percentages, including an average of 85 percent.',
              'The results compare these specific information messages in a campus referendum setting. '
              'Connections to charitable giving or other environmental initiatives are applications to '
              'consider, not outcomes observed in the experiment.'],
  'data': 'Online survey of 559 students at one Midwestern liberal arts university in October 2011. '
          'Random assignment created control, fee-amount, participation and combined-message groups of '
          '218, 108, 113 and 120. Administrative data for the broader student population support '
          'selection-model checks.',
  'method': 'Randomized survey information treatments for a hypothetical green-fee referendum. Analysis '
            'uses mean comparisons, OLS, maximum-likelihood interval regressions for payment-card '
            'responses, and selection models incorporating administrative student data.',
  'whats_new': 'Compares information about participation with information about contribution amounts in '
               'a public-good referendum, and checks the treatment estimates using administrative data '
               'on survey participation.',
  'audiences': ['Behavioral and environmental economists working on social norms and nudges',
                'Public-goods and charitable-giving experimentalists',
                'Campus sustainability offices and green-fee organizers',
                'Stated-preference methodologists'],
  'related': [('Allcott, H. (2011). Social norms and energy conservation. Journal of Public Economics '
               '95(9–10): 1082–1095.',
               None),
              ('Goldstein, N. J., R. B. Cialdini and V. Griskevicius (2008). A room with a viewpoint: '
               'using social norms to motivate environmental conservation in hotels. Journal of '
               'Consumer Research 35(3): 472–482.',
               None),
              ('Frey, B. S. and S. Meier (2004). Social comparisons and pro-social behavior: testing '
               '‘conditional cooperation’ in a field experiment. American Economic Review 94(5): '
               '1717–1722.',
               None),
              ('Shang, J. and R. Croson (2009). A field experiment in charitable contribution: the '
               'impact of social information on the voluntary provision of public goods. Economic '
               'Journal 119(540): 1422–1439.',
               None),
              ('Alpizar, F., F. Carlsson and O. Johansson-Stenman (2008). Does context matter more for '
               'hypothetical than for actual contributions? Experimental Economics 11(3): 299–314.',
               None)],
  'versions': [('Published article (Taylor & Francis)', 'https://doi.org/10.1080/00036846.2015.1080803'),
               ("Published PDF in the author's repository",
                'https://raw.githubusercontent.com/yangguanyi/Published/main/2016_AE_Meyer_Yang.pdf'),
               ('RePEc listing', 'https://ideas.repec.org/f/pya376.html')],
  'questions': [['Which social-norm message increased support for the campus green fee?',
                 'In this experiment, the high-participation message raised the maximum fee students '
                 'said they would approve by about $7 per semester. The fee-amount message reduced it '
                 'by about $8.50. The experiment tests these messages at one university, not a '
                 'universal rule about fundraising.'],
                ['Were these actual contributions?',
                 'No. Students selected the largest fee they would support in a hypothetical '
                 'referendum. If adopted, the fee would apply to all students; actual payments and '
                 'donations were not observed.']],
  'funding': None,
  'short_summary': 'A randomized survey compares participation messages with fee-amount messages in a '
                   'hypothetical campus environmental referendum.',
  'reviewed_on': '2026-11-09',
  'pdf_path': 'papers/social-norms-information-green-fee/paper.pdf',
  'pdf_label': 'Read published paper (PDF)',
  'version_note': 'Summary based on the published article linked here. Earlier working-paper versions '
                  'are listed separately below.',
  'publication_date': '2016-01-26',
  'volume': '48',
  'issue': '5',
  'first_page': '389',
  'last_page': '401',
  'online_date': '2015-09-11'},
 {'slug': 'schooling-disutility',
  'kind': 'article',
  'theme': 'college-lifecycle',
  'title': 'How Much Does Schooling Disutility Matter?',
  'authors': [('Guanyi Yang', 'Colorado College (St. Lawrence University at publication)'),
              ('Ben Casner', 'Federal Trade Commission')],
  'year': 2021,
  'venue': 'Research in Economics',
  'venue_detail': 'Vol. 75, No. 1, pp. 87–95',
  'doi': '10.1016/j.rie.2020.11.004',
  'jel': ['D11', 'I2', 'J24'],
  'keywords': ['structural estimation',
               'human capital theory',
               'disutility of schooling',
               'education choices',
               'precautionary saving',
               'risk'],
  'one_liner': 'A schooling disutility term changes how wealth and risk enter education decisions. In a '
               'two-period model, it can make a common increase in future consumption risk raise the '
               'incentive to study through precautionary saving, even though people remain risk averse.',
  'abstract': 'Studies on structural education choice models are often inconsistent in choosing whether '
              'and how to include a disutility of education, especially in an environment with risk and '
              'wealth inequality. We show that adding a disutility term to the education decision, a '
              'human capital investment option, is equivalent to assuming a relationship between '
              'wealth, risk, and education. Utility gain from education is increasing in the riskiness '
              'of future consumption. A riskier environment further propels an agent to choose the '
              'human capital investment option that maximizes future income. If the degree of risk '
              'increases heterogeneously across multiple human capital investment options, risk '
              'aversion and the precautionary savings motive can compound or negate each other '
              'depending on which option has a greater increase in risk.',
  'findings': ['Proposition 1: if schooling has a positive financial return and marginal utility is '
               'convex (precautionary saving), a mean-preserving spread in future consumption risk '
               'raises the utility return to education.',
               'Proposition 2: if both schooling and working become riskier but schooling’s risk rises '
               'by not too much more, the precautionary-saving effect still dominates risk aversion and '
               'schooling becomes more attractive.',
               'The utility return to education is decreasing in initial wealth (extending Belley and '
               'Lochner 2007 to a risky environment), so the range of human capital for which an agent '
               'chooses school narrows with wealth.',
               'Implication for estimation: counterfactuals from models that include a disutility term '
               'embed these wealth–risk–schooling relations by assumption; models that omit it may '
               'understate the role of wealth and risk.'],
  'limits': ['A two-period decision model without general equilibrium, bankruptcy, or estimation; '
             'disutility is held constant rather than varying with human capital.',
             'This is a theoretical result under stated preference and risk assumptions, not an '
             'estimated effect of risk on actual enrollment.',
             'An increase only in education-specific risk need not raise schooling incentives.'],
  'context': ['The paper is agnostic about whether students actually experience disutility; its point '
              'is the consequence of including or excluding the term in structural work.',
              'Previously circulated as “The Relationship Between Disutility of Education, Wealth, and '
              'Schooling Decisions”.'],
  'data': 'None (theoretical).',
  'method': 'Two-period model of schooling versus work with consumption-saving choice, CRRA utility in '
            'the numerical example, mean-preserving spreads following Rothschild and Stiglitz (1970), '
            'and envelope-theorem proofs.',
  'whats_new': 'Identifies the implicit assumptions introduced by a schooling disutility term in '
               'structural models and adds the precautionary-saving (third-derivative) channel to the '
               'risk-and-schooling literature.',
  'audiences': ['Structural labor and education economists',
                'Quantitative macroeconomists building life-cycle models with human capital',
                'Theorists of human capital investment under uncertainty'],
  'related': [('Belley, P. and L. Lochner (2007). The changing role of family income and ability in '
               'determining educational achievement. Journal of Human Capital 1(1): 37–89.',
               None),
              ('Levhari, D. and Y. Weiss (1974). The effect of risk on the investment in human capital. '
               'American Economic Review 64(6): 950–963.',
               None),
              ('Hartog, J. and L. Diaz-Serrano (2015). Why do we ignore the risk in schooling '
               'decisions? De Economist 163(2): 125–153.',
               None),
              ('Leland, H. E. (1968). Saving and uncertainty: the precautionary demand for saving. '
               'Quarterly Journal of Economics 82(3): 465–473.',
               None),
              ('Yang, G. (2025). Better late than never: macroeconomic impact of intermittent college '
               'enrollment and tuition subsidies. Journal of Economic Dynamics and Control 181: 105219.',
               '10.1016/j.jedc.2025.105219')],
  'versions': [('Published article (Elsevier)', 'https://doi.org/10.1016/j.rie.2020.11.004'),
               ("Published PDF in the author's repository",
                'https://raw.githubusercontent.com/yangguanyi/Published/main/2021_RIE_Casner_Yang.pdf'),
               ('RePEc listing', 'https://ideas.repec.org/f/pya376.html')],
  'questions': [('Can more risk increase the incentive to study?',
                 "Under the model's assumptions, a common increase in future consumption risk can raise "
                 'the utility return to education through precautionary saving. An increase in the risk '
                 'of education alone can instead discourage schooling. The paper derives these '
                 'comparative statics rather than estimating an enrollment effect.')],
  'funding': None,
  'short_summary': 'A theoretical analysis shows how the psychic cost of schooling changes the '
                   'relationship between wealth, risk and education decisions.',
  'reviewed_on': '2026-11-09',
  'pdf_path': 'papers/schooling-disutility/paper.pdf',
  'pdf_label': 'Read published paper (PDF)',
  'version_note': 'Summary based on the published article linked here. Earlier working-paper versions '
                  'are listed separately below.',
  'publication_date': '2021-03',
  'volume': '75',
  'issue': '1',
  'first_page': '87',
  'last_page': '95',
  'online_date': '2020-12-03'},
 {'slug': 'college-major-chinese-immigrants',
  'kind': 'article',
  'theme': 'college-lifecycle',
  'title': 'The Effect of College Major on Labor Market Outcomes of Chinese Immigrants: An Examination '
           'of Undergraduate Major Choices and Their Impact on Employment and Earnings',
  'authors': [('Guanyi Yang',
               'Colorado College (Ohio Wesleyan University and Ohio State University at publication)')],
  'year': 2015,
  'venue': 'Journal of the Knowledge Economy',
  'venue_detail': 'Vol. 6, No. 4, pp. 1138–1162 (published online 28 March 2014)',
  'doi': '10.1007/s13132-014-0199-2',
  'jel': ['J15', 'J24', 'J61', 'I23'],
  'jel_note': 'The published article does not print JEL codes; the codes here were added for this page.',
  'keywords': ['labor', 'immigration', 'higher education', 'human capital', 'Asian immigrants'],
  'one_liner': 'Using the 2009 American Community Survey, this paper documents college-major choices '
               'and their association with employment and annual earnings among college-educated '
               'Chinese immigrant men. Several popular majors also rank highly in fitted labor-market '
               'outcomes, but these cross-sectional associations do not identify the causal return to '
               'choosing a major.',
  'abstract': 'Education is a crucial factor that determines labor market outcomes, especially for '
              'immigrants. This paper specifically examines the undergraduate major choice for Chinese '
              'immigrants and its relationship to their labor market outcome. Compared to other Asian '
              'groups and the mainstream society, Chinese immigrants are uniquely congregated in '
              'business and science categories. The level of popularity to a major is positively '
              'related to their labor market outcome. This finding reveals the current premarket '
              'educational investment pattern for Chinese immigrants and adds to the existing '
              'literature by focusing on how detail education quality in terms of major relates to '
              'labor market performance.',
  'findings': ["In the paper's unweighted descriptive sample, major shares are 35.7 percent "
               'engineering, 13.9 percent mathematics and computer science, 12.6 percent business, 10.2 '
               'percent physical science, and 8.5 percent biology and life science (Table 5).',
               'An omnibus test finds that major composition differs across the Chinese, Japanese, '
               'Korean and native-born non-Hispanic white comparison groups. It does not establish a '
               'separate tested difference for every pair of groups.',
               'Biology and life science, physical science, and mathematics and computer science appear '
               'among both the five most popular majors and the five highest fitted employment '
               'probabilities. These probabilities depend on the example covariate profile used in the '
               'paper (Tables 5, 7 and 11).',
               'The employment model uses 3,990 Chinese immigrant men. Separate annual-earnings models '
               'use 3,209 Chinese, 699 Japanese, 1,381 Korean and 14,232 native-born non-Hispanic white '
               'men, restricted to those who worked more than 40 weeks in the previous year (Table 2).'],
  'limits': ["Historical 2009 ACS data on men aged 25 to 70 with at least a bachelor's degree. "
             'Descriptive shares are unweighted.',
             'Employment and earnings regressions are observational. Differences can reflect selection '
             'into majors, occupations, education and immigration; the paper does not identify causal '
             'returns to changing a major.',
             'The earnings outcome is prior-year annual pretax wage and salary income among those who '
             "worked more than 40 weeks. It is not an hourly wage or a prediction for today's "
             'graduates.'],
  'context': ['The paper separates Chinese immigrants from the broader Asian-American category and '
              'distinguishes fields of study rather than considering only years of education.',
              'Employment predictions in Table 7 hold characteristics at an example profile. They are '
              'not average job-finding probabilities for new graduates.'],
  'data': "2009 ACS 1 percent microdata via IPUMS; men aged 25 to 70 with at least a bachelor's degree. "
          'The paper groups 38 ACS major categories into 15 fields. Earnings regressions restrict the '
          'sample to more than 40 weeks worked in the previous year.',
  'method': 'Logit employment models and separate log-linear annual wage-and-salary earnings '
            'regressions by group. Employment controls include degree, age, years in the US, English '
            'proficiency, family status, citizenship and geography; earnings models additionally '
            'include occupation and self-employment.',
  'whats_new': 'Separates Chinese immigrants from the broader ‘Asian American’ category and links field '
               'of study to employment and pay.',
  'audiences': ['Immigration and labor economists',
                'Researchers on college major choice and returns to field of study',
                'Asian American studies'],
  'related': [('Xie, Y. and K. Goyette (2004). A Demographic Portrait of Asian Americans. Russell Sage '
               'Foundation and Population Reference Bureau.',
               None),
              ('Black, D., A. Haviland, S. Sanders and L. Taylor (2006). Why do minority men earn less? '
               'A study of wage differentials among the highly educated. Review of Economics and '
               'Statistics 88(2): 300–313.',
               None),
              ('Chiswick, B. R. and P. W. Miller (2009). The international transferability of '
               'immigrants’ human capital. Economics of Education Review 28(2): 162–169.',
               None)],
  'versions': [('Published article (Springer)', 'https://doi.org/10.1007/s13132-014-0199-2'),
               ("Published PDF in the author's repository",
                'https://raw.githubusercontent.com/yangguanyi/Published/main/2015_JKE_Yang.pdf'),
               ('RePEc article record',
                'https://ideas.repec.org/a/spr/jknowl/v6y2015i4p1138-1162.html')],
  'questions': [('Does the study estimate the causal payoff to choosing a major?',
                 'No. It documents historical major choices and conditional employment and '
                 'annual-earnings associations. The design does not eliminate selection into majors or '
                 'establish what would happen if an individual changed fields.')],
  'funding': 'Norman Leonard Research Grant, Department of Economics, Ohio Wesleyan University.',
  'short_summary': 'Historical ACS data describe college majors and their association with employment '
                   'and annual earnings among Chinese immigrant men.',
  'reviewed_on': '2026-11-09',
  'pdf_path': 'papers/college-major-chinese-immigrants/paper.pdf',
  'pdf_label': 'Read published paper (PDF)',
  'version_note': 'Summary based on the published article linked here. Earlier working-paper versions '
                  'are listed separately below.',
  'publication_date': '2015-12',
  'volume': '6',
  'issue': '4',
  'first_page': '1138',
  'last_page': '1162',
  'online_date': '2014-03-28'}]

# Public project titles only, pending author-supplied drafts.
IN_PROGRESS = [{'slug': 'time-inequality-household-dynamics',
  'title': 'Not Lazy, Just Busy: Time Inequality and Household Dynamics',
  'coauthors': 'Konstantin Platonov and Michael Carter',
  'theme': 'college-lifecycle',
  'status': 'Draft forthcoming'},
 {'slug': 'monetary-policy-fiscal-transfers-race-hank',
  'title': 'Same Stimulus, Opposite Incidence: Monetary Policy, Fiscal Transfers, and Race in HANK',
  'coauthors': 'EJ Ume',
  'theme': 'race-macro',
  'status': 'Draft forthcoming'},
 {'slug': 'china-college-supply-shock',
  'title': 'Absorbing a College Supply Shock: Where Did the Adjustment Go?',
  'coauthors': 'Xuan Jiang',
  'theme': 'china-education',
  'status': 'Draft forthcoming'},
 {'slug': 'night-light-pregnancy-infant-health',
  'title': 'Artificial Night Light Exposure During Pregnancy and Infant Health',
  'coauthors': 'Andrés Azqueta-Gavaldón and Ella Reese-Clauson',
  'theme': 'night-sky',
  'status': 'Draft forthcoming'}]

THEMES = {'night-sky': {'title': 'Economics of the night sky',
               'blurb': 'Research on the economic value of dark skies and the consequences of light '
                        'pollution. The published Great Sand Dunes study combines visitor surveys, '
                        'satellite nightlight and recreation-demand models. Work on prenatal light '
                        'exposure and infant health is in progress.'},
 'college-lifecycle': {'title': 'Human capital, household choices and labor-market risk',
                       'blurb': 'How education choices, household resources and labor-market risk '
                                'interact over a lifetime. These papers examine flexible college '
                                'access, schooling disutility, college majors and temporary employment. '
                                'Work on time inequality and household dynamics is in progress.'},
 'race-macro': {'title': 'Racial disparities in labor markets and wealth',
                'blurb': 'Quantitative macroeconomic research on racial differences in labor-market '
                         'opportunities and wealth accumulation. The available working paper studies '
                         'hiring discrimination in a search model; a separate project examines monetary '
                         'policy and fiscal transfers in a HANK model.'},
 'emerging-markets': {'title': 'Emerging markets: informality and global financial shocks',
                      'blurb': 'Research with Jaroslav Horvath on emerging-market business cycles, '
                               'informal employment, and the transmission of global financial risk '
                               'through capital flows, equity returns and borrowing spreads.'},
 'china-education': {'title': 'Education and families in China',
                     'blurb': 'Research on sibling education spillovers and the tradeoff between '
                              "migrant parents' time and financial resources in rural China. Work on "
                              'the expansion of college supply is in progress.'},
 'behavior-public-goods': {'title': 'Behavior and public goods',
                           'blurb': 'Experimental evidence on how information about peer participation '
                                    'and contribution amounts changes stated support for environmental '
                                    'public goods.'}}
