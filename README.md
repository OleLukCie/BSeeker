# BSeeker

A book e-commerce data collection and analysis project developed based on the *Python Scrapy framework*. It implements targeted web crawling, data deduplication & cleaning, structured data processing and visual data analysis, covering the full workflow of crawler development, data processing and business data analysis.

| Tech Stack               | Details                    |
| ------------------------ | -------------------------- |
| Language                 | Python                     |
| Crawler Framework        | Scrapy                     |
| Data Processing          | Pandas                     |
| Data Visualization       | Matplotlib                 |
| Containerization         | Docker                     |
| Configuration Management | python-dotenv              |
| DBMS                     | SQLite                     |
| Frontend                 | jQuery    ECharts    Flask |

## Data Sources

Targeted crawling of core book information from e-commerce platforms:

- Book Name
- Author
- Publisher
- Price
- Rating Score
- Sales Volume

## Core Features

- Efficient multi-page data crawling, deduplication and data cleaning via Scrapy
- Structured data sorting and storage with Pandas
- Data visual analysis implemented by Matplotlib
- Business insight mining including book pricing rules, mainstream publisher distribution and sales volume distribution

## Deployment

```bash
docker-compose up --build
```

### Full Data Workflow (Crawling → Cleaning → Analysis → Visualization → Storage)

```bash
docker-compose exec bseeker python run.py
```

### Launch Frontend Dashboard

```bash
cd D:\BSeeker\panel
python api.py
```

*The dashboard will automatically read and display data from `data/db/bseeker.db`.*

***Dashboard Features***

- *Statistics Cards: Total Books, Average Price, Average Rating, Number of Categories*
- *Price Distribution Chart: ECharts Bar Chart*
- *Rating Distribution Chart: ECharts Bar Chart*
- *Top 10 Popular Categories: ECharts Horizontal Bar Chart*
- *Top 10 Popular Publishers: ECharts Horizontal Bar Chart*
- *Latest Books Table: Top 20 Records*

### Force Re-crawl All Data

```bash
docker-compose exec bseeker python run.py --force-crawl
```

## License

MIT License