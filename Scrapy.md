# Scrapy Architecture

![Scrapy.png](.\img\Scrapy.png)

**Scrapy Engine**: Responsible for communication, signals, and data transmission among Spider, ItemPipeline, Downloader, and Scheduler.

**Scheduler**: It is responsible for receiving Request requests sent by the engine, organising and arranging them in a certain way, queuing them, and returning them to the engine when needed.

**Downloader**: Responsible for downloading all Requests sent by the Scrapy Engine and returning the obtained Responses to the Scrapy Engine, which then passes them to the Spider for processing.

**Spider**: It is responsible for handling all responses, extracting data from them, obtaining the data required for Item fields, and submitting URLs that need to be followed up to the engine, which then enters the Scheduler again.

**Item Pipeline**: It is responsible for processing the Items obtained by the Spider and performing subsequent processing (detailed analysis, filtering, storage, etc.).

**Downloader Middlewares**: You can think of it as a component that allows you to customise and extend download functionalities.

**Spider Middlewares**: You can understand them as functional components that can be custom extended and operate the communication between the engine and the Spider (for example, incoming Responses to the Spider and outgoing Requests from the Spider).

---

*The entire programme will only stop when there are no requests left in the scheduler, that is to say, Scrapy will retry downloading URLs that failed.*

---

- Create a project: Create a new web scraping project

- Define the goal: Clearly define what you want to scrape

- Create the scraper: Build the scraper to start crawling web pages

- Store content: Design a pipeline to store the scraped content

---
