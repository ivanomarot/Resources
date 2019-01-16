# AWS Big Data Guide

## Data Collection

You have configured an application that batches up data on the servers before submitting it for intake. Your front-end or application server failed, and now you have lost log data. How can you prevent this from occurring in the future while still ensuring that you will have rapid access to your data from multiple different applications?

````
Submit system and application logs directly to Amazon Kinesis Streams using the Kinesis agent on the front-end and application machines themselves.

Why is this correct?
Correct. With Amazon Kinesis Streams, you can have producers push data directly into an Amazon Kinesis stream. For example, you can submit system and application logs to Amazon Kinesis Streams and access the stream for processing within seconds. This prevents the log data from being lost if the front-end or application server fails, and reduces local log storage on the source. Amazon Kinesis Streams provides accelerated data intake because you are not batching up the data on the servers before you submit it for intake.

Further Reading: https://d0.awsstatic.com/whitepapers/Big_Data_Analytics_Options_on_AWS.pdf

````

---

Your company releases new features with high frequency while demanding high application availability. As part of the application's A/B testing, logs from each updated Amazon EC2 instance need to be analyzed in near real-time to ensure that the application is working flawlessly after each deployment. If the logs show any abnormal behavior, then the application version of the instance is changed to a more stable one. Which of the following methods should you use for shipping and analyzing the logs in a highly-available manner?

````
Ship the logs to an Amazon Kinesis stream and have the consumers analyze the logs in a live manner.
````

---

What combination of services do you need for the following requirements: accelerate petabyte-scale data transfers, load streaming data, and the ability to create scalable, private connections. Select the correct answer order.

````
Snowball, Kinesis Firehose, Direct Connect
````

---

You have EC2 instances that you need to connect to your on-premises data center. You need to be able to support a connection speed of 200 Mbps. How should you configure this?

````
Provision a VPN connection between a VPC and data center, Submit a Direct Connect partner request to provision cross-connects between your data center and the Direct Connect location, then cut over from the VPN connection to one or more Direct Connect connections as needed.
````

---

You need to analyze clickstream data on your website from multiple applications. You want to analyze the pattern of pages a consumer clicks on and in what order. You need to be able to use the data in real time and want to manage as little infrastructure as possible. Which option would meet this requirement?

````
Use Amazon Kinesis with a worker to process the data received from the Kinesis stream.
````

---

You need a secure, dedicated connection from your data center to AWS so you can use additional compute resources (EC2) without using the public internet. Which is your best option?

````
Direct Connect
````

---

You currently have an on-premises Oracle database and have decided to leverage AWS and use Aurora. You need to do this as quickly as possible. How do you achieve this?

````
Use AWS Data Migration Services and create a target database, migrate the database schema, set up the data replication process, initiate the full load and a subsequent change data capture and apply, and conclude with a switch-over of your production environment to the new database once the target database is caught up with the source database.
````

---

There is a 14-day backpacking tour across Europe. The tour coordinators are using a Kinesis Data Stream and IoT sensors to monitor the movement of the group. You have changed the default settings on the stream to the max settings. Each backpack has a sensor and data is getting back to the stream with the default stream settings. On the last day of the tour, data is sent to S3. When you go to interpret the data in S3, there is only data for 7 days. Which of the following is the most probable cause of this?

````
Data records are only accessible up to 7 days from the time they are added to a stream.
````

---

Does AWS Direct Connect allow you access to all Availability Zones within a region?

````
Yes
````

---

There is a five-day car rally race across Europe. The race coordinators are using a Kinesis stream and IoT sensors to monitor the movement of the cars. Each car has a sensor and data is getting back to the stream with the default stream settings. On the last day of the rally, data is sent to S3. When you go to interpret the data in S3, there is only data for the last day and nothing for the first 4 days. Which of the following is the most probable cause of this?

````
Data records are only accessible for a default of 24 hours from the time they are added to a stream.

Why is this correct?
Correct. Streams support changes to the data record retention period of your stream. An Amazon Kinesis stream is an ordered sequence of data records, meant to be written to and read from in real-time. Data records are therefore stored in shards in your stream temporarily. The period from when a record is added to when it is no longer accessible is called the retention period. An Amazon Kinesis stream stores records for 24 hours by default, up to 168 hours.
````

---

Your IoT application has smoke sensors in various hotels. You need to collect this data in real-time and log it all to S3 and, in the event a sensor detects smoke, to send out an alert. What steps do you need to take to accomplish this?

````
Create a rule to filter the smoke sensors that detect smoke.
Create an action to send a push notification to all users using Amazon SNS.
````

## Data Storage

An application requires a highly available relational database with an initial storage capacity of 8 TB. The database will grow by 8 GB every day. To support expected traffic, at least eight read replicas will be required to handle database reads. With what service could you meet these requirements?

````
Amazon Aurora
Why is this correct?
Yes! Aurora can have up to 15 read replicas! https://aws.amazon.com/rds/aurora/
````

---

Your company is designing a web application using stateless web servers. Which services would work to store session state data?

````
DynamoDB
ElastiCache
````

---

Your client has a high-volume DynamoDB table that serves comment information to an internal API. Currently, the table allows you to query with a composite primary key with postId as a hash key and commentId as a sort key. Application validation ensures that each item has other fields including timestamp, userId, and sentimentScore. The client has several long-running users, and they would like to provide more effective ways of surfacing posts from them from different time frames. How might the client enable this sort of functionality?

````
Create a Global Secondary Index with a hash key of userId and a sort key of timestamp.
````

Your company creates mobile games that use DynamoDB as the backend data store to save the high scores. There is a hash and range key on the main table, where the game is the partition key and the username is the sort key. Your highest selling game customers complain that your game slows down to a halt when trying to send the high scores to your backend. CloudWatch metrics suggest you are not exceeding your provisioned WCUs. Your company is currently undergoing an in-depth re-platforming and is wondering how they can improve this situation in the long term. Which option can improve the user experience without increasing costs?

````
Recreate the table with the username as the partition key and the game as the sort key.
````

---

You work for a social media start-up and need to analyze the effectiveness of your new marketing campaign from your previous one. Which process should you use to record the social media replies in a durable data store that can be accessed at any time for analytics of historical data?

````
Read the data from the social media sites, store it in DynamoDB, and use Apache Hive with Amazon Elastic MapReduce for analytics.
````

---

Your mobile application uses a DynamoDB backend to log data. The table has 3 GB of data already in it. The primary key/index is on the device ID of the mobile phone. The application also logs the location of the mobile phone. A new marketing campaign requires a quick lookup for all the phones in a particular area. Also, you have checked CloudWatch, and you are using 90% of the provisioned RCUs and WCUs. How do you make sure you can support the new campaign without any downtime?

````
Create a GSI on location.
Increase the RCUs.
Increase the WCUs.
````

---

You have created a DynamoDB table with CustomerID as the primary key for the table. You need to find all customers that live in a particular ZIP code. How should you configure this?

````
Use ZipCode as the partition key for a global secondary index, since there are a lot of ZIP codes and you will probably have a lot of customers.

Global secondary indexes are particularly useful for tracking relationships between attributes that have a lot of different values. For example, you could create a DynamoDB table with CustomerID as the primary partition key for the table and ZipCode as the partition key for a global secondary index, since there are a lot of ZIP codes and you will probably have a lot of customers. Using the primary key, you could quickly get the record for any customer. Using the global secondary index, you could efficiently query for all customers that live in a given ZIP code.
````

---

You need to leverage Amazon Simple Storage Service (S3) for backups using third-party software. How can you ensure the credentials provisioned for the third-party software limit access to the backups-18 folder of the abc-corp-backups-2018 bucket to allow that third party to send data into the bucket from another AWS account?

````
A custom bucket policy on the abc-corp-backups-2018 bucket limited to the Amazon S3 API in the backups-18 folder. Specify the principal of the other AWS account.
````

---

You have been asked to ensure that all AWS API calls are collected across your company's AWS account and that they are kept around for 90 days for analysis. After that, they must be able to be restored for 3 years. How can you meet these needs in a scalable, cost-effective way?

````
Enable CloudTrail logging to a centralized S3 bucket, set a lifecycle policy to move the data to Glacier after 90 days, and expire the data after 3 years.
````

----

Your sales team uploads sales figures daily. You're designing a solution that has durable storage for these sales figure documents that will also protect against accidental deletions of important documents. Which of these solutions could meet these needs?

````
Store data in an S3 bucket and enable versioning.
````

You have a 500-GB file in Amazon S3. Each night, you run a COPY command into a 10-node Redshift cluster. How could you prepare the data in order to make the COPY command more performant?

````
Split the file into 500 smaller files.
Compress the file using gz compression.
````

## Data Processing

Your steaming application requires only-once delivery and out-of-order data is acceptable as long as the data is processed within 5 seconds. Which solution can be used?

````
Spark Streaming
Spark has micro-batching but can guarantee only-once-delivery if configured correctly.
````

---

You work for a retail chain that collects point-of-sale data from all stores four times a day to get sales statistics and to plan personnel schedules based on how busy the store is. Each store runs independently and thus might have different data in terms of structure and format which comes in at different frequency during the day. The expected size of the data is generally small but might be high velocity depending on how busy the store is. The ETL and processing need to be done on an event-driven basis at the time the data is received. The data needs to be processed with several transformations and finally stored in a database where complex queries can be run against it. Which option would be the best solution, especially knowing that you do not have a team of people to manage the infrastructure behind it all and a limited budget?

````
Transfer the data from the stores to S3, use lambda to validate and load the data in batches into an EMR/Spark cluster, load the output into Redshift for analysis, and turn off the EMR cluster after business hours
````

---

You need a fast, fully managed, petabyte-scale data warehouse that makes it simple and cost-effective to analyze all of your data using your existing business intelligence tools. Which Big Data tool should you use?

````
Redshift
````

---

You have a customer-facing application running on multiple M3 instances in two AZs. These instances are in an auto-scaling group configured to scale up when load increases. After taking a look at your CloudWatch metrics, you realize that during specific times every single day, the auto-scaling group has a lot more instances than it normally does. Despite this, one of your customers is complaining that the application is very slow to respond during those time periods every day. The application is reading and writing to a DynamoDB table which has 400 Write Capacity Units and 400 Read Capacity Units. The primary key is the company ID, and the table is storing roughly 20 TB of data. Which solution would solve the issue in a scalable and cost-effective manner?

````
Use data pipelines to migrate your DynamoDB table to a new DynamoDB table with a different primary key that evenly distributes the dataset across the table

Redistributing this table data more effectively in a new table should increase performance. Data Pipeline is the best solution to migrate existing DynamoDB table data to a new table.
````

---

You need to create a recommendation engine for your e-commerce website that sells over 300 items. The items never change and the new users need to be presented with the list of all 300 items in order of their interest. Which option do you use to accomplish this? (Choose all that apply)

````
Mahout
Spark/SparkMLlib

Amazon Machine Learning cannot be chosen due to limited number of recommendations
````

---

What are some of the benefits of running Spark vs. MapReduce?

````
Spark can use in-memory processing to speed up queries.
Machine learning and streaming libraries are included with Spark.
````

---


You work for a photo processing start-up and need the ability to change an image from color to grayscale after it has been uploaded to Amazon S3. How can you configure this in AWS without having to deal with persistent infrastructure?

````
Real-time file processing – you can trigger Lambda to invoke a process where a file has been uploaded to Amazon S3 or modified.
````

---

Your company has decided to use the Amazon Machine Learning service to classify social media posts mentioning your company into two categories: posts requiring a response and posts that do not. You have access to a training dataset of 20,000 posts that each contain things like the timestamp, author, and the full text of the post. You are missing the target labels that are required for training. How can you effectively create valid target label data?

````
Ask the social media handling team to review each post and provide the label.
Use the Amazon Mechanical Turk web service to publish Human Intelligence Tasks that ask Turk workers to label the posts.
````

---

You have a Kinesis stream with four shards that is getting data from various IoT devices. There is a lambda transformation function attached to the streams that fan out the data to eight destinations. How many lambda functions get invoked concurrently per record?

````
4
````

---

You need to be able to access resources in S3 and then write data to tables in S3. You also need to be able to load table partitions automatically from Amazon S3. Which Big Data tool enables you to do so?

````
EMR and Hive

Correct. Hive allows user extensions via user-defined functions written in Java. Amazon EMR has made numerous improvements to Hive, including direct integration with DynamoDB and Amazon S3. For example, with Amazon EMR you can load table partitions automatically from Amazon S3, you can write data to tables in Amazon S3 without using temporary files, and you can access resources in Amazon S3, such as scripts for custom map and/or reduce operations and additional libraries.

https://d0.awsstatic.com/whitepapers/Big_Data_Analytics_Options_on_AWS.pdf
````

---

Your enterprise application requires key-value storage as the database. The data is expected to be about 10 GB the first month and grow to 2 PB over the next two years. There are no other query requirements at this time. What solution would you recommend?

````
HBase on HDFS
````

## Data Analysis


A new client is requesting a tool that will provide fast query performance for enterprise reporting and business intelligence workloads, particularly those involving extremely complex SQL with multiple joins and sub-queries. They also want the ability to give analysts access to a central system through tradition SQL clients that allow them to easily explore and familiarize themselves with the data. What solution do you initially recommend they investigate?

````
Redshift
````

---

Your company deployed 100 sensors to measure traffic speeds on various highways that generated about 4 GB of data per month. The initial architecture used 400 GB RDS with EC2 instances. Over the next 3 months, there will be an additional 100,000 sensors added. You need to retain the data for at least 2 years for trends reporting. Which is the best solution to accomplish this?

````
Replace the RDS instance with a 6 node Redshift cluster with 96 TB of storage.
````

---

Your data warehouse is running on Redshift. You need to ensure that your cluster can be restored in another region in case of region failure. What actions can you take to ensure that?

````
Enable snapshot replication to another region.

Creating EBS snapshots for Redshift is not possible. Manual snapshots would be in the same region and automatic cross-region replication for Redshift is not a current feature.
````

---

You have been tasked to create an enterprise data warehouse. The data warehouse needs to collect data from each of the three channels’ various systems and from public records for weather and economic data. Each data source sends data daily for consumption by the data warehouse. Because each data source may be structured differently, an extract, transform, and load (ETL) process is performed to reformat the data into a common structure. Then, analytics can be performed across data from all sources simultaneously. Which tools shall you implement?

````
S3, EMR, Redshift, QuickSight

The first step in this process is getting the data from the many different sources onto Amazon S3. Amazon EMR is used to transform and cleanse the data from the source format into the destination and a format. Each transformation job then puts the formatted and cleaned data onto Amazon S3. Amazon Redshift loads, sorts, distributes, and compresses the data into its tables so that analytical queries can execute efficiently and in parallel. For visualizing the analytics, Amazon QuickSight can be used, or one of the many partner visualization platforms via the OBDC/JDBC connection to Amazon Redshift.
````

---

You need to perform ad-hoc SQL queries on structured data that will be generated by a fleet of IoT devices about every 20 minutes. What services should you use if you want to be able to also compare this incoming data with a massive amount of existing data inside one centralized data warehouse?

````
Kinesis Firehose and Redshift
````

---


You have large volumes of structured data in DynamoDB that you want to persist and query using standard SQL and your existing BI tools. What solution should you use?

````
Use the COPY command to load data in parallel directly to Redshift from DynamoDB
````

---

Which tool allows you to search through CloudWatch logs?

````
Elasticsearch
````

---

You need to analyze a large set of JSON data from Kinesis and DynamoDB by querying for a variety of different values inside of the documents to search for particular records. The fields you need to query, and the records themselves, vary significantly. Which Big Data tool should you use if your organization is trying to use more managed services when possible?

````
Elasticsearch
````

---


A client comes to you and requests access to a specific Redshift compute node that they want access to in order to add performance monitoring software. They plan to install open source software on this node in order to have access to data such as disk utilization and query performance. How do you address the request?

````
You inform them that directly connecting is not possible, but that the AWS console and CloudWatch provide many of the metrics.
````

---

You have a lot of data (over 50 TB) in your on-premises data warehouse that you need to load into Amazon Redshift. Which option would allow you to load this data in Redshift?

````
Snowball into S3 then COPY to Redshift.
````

---

You have 30 GB of data that needs to be loaded into Redshift. Which of the following will speed up the data ingestion? You also want to be sure that the data lives in more than one place inside of AWS anyway.

````
Store the data already sorted in the sortkey order.
Compress the data inside of S3 before loading it into Redshift.
Copy the data to S3 and use COPY to move the data into Redshift.
````


## Data Visualization

You've been asked by the VP of People to showcase the current breakdown of the headcount for each department within your organization. What chart do you select to do this in order to make it easy to compare each department?

````
A pie chart

In this example, you need to compare a static dataset that makes up a whole. A pie chart is an appropriate chart for this purpose.
````

---

You are attempting to determine if there is any relationship between certain marketing expenditures and the performance of your products. You decide the best way to visualize this is with what kind of chart?

````
Scatter Plot
````

---

You've been asked by management to bucket customers who are currently in different phases of onboarding. They'd like to see the number of customers in each phase. What sort of visualization do you use?

````
A histogram
````

---

You need to visualize data from Spark and Hive running on an EMR cluster. Which of the options is best for an interactive and collaborative notebook for data exploration?

````
Zeppelin
````

---

You've been asked to select a tool that can easily visualize sales data that comes in as JSON to S3, occasionally as ad-hoc CSV files, and even from the Amazon Redshift data warehouse. The solution must allow multiple users from the finance department to easily access it and occasionally upload their own Excel spreadsheets to compare with existing data. What solution do you recommend?

````
QuickSight and a combination of data source connections with the Redshift cluster and existing S3 JSON documents while still allowing finance to upload files directly.

This solution can easily accomplish all the requirements without the extra work of integrating a bunch of extra tools. Also, QuickSight also supports XLSX files by default!
````

---

You've been asked to find a solution to visualize company JIRA data alongside GitHub PRs in a way that minimizes developer time. What solution do you propose?

````
Pull JIRA and GitHub data into QuickSight and build visualizations on top of those data sources.
````

---

You have a JSON data file in S3 that you are attempting to load into JavaScript visualization you are writing locally. This visualization makes an HTTP GET request to the S3 location that fails. However, when you attempt to visit the URL being requested by the JavaScript directly from inside your browser it seems to be loading fine. You are also using a private/incognito window and are not signed into the AWS console. What is the most likely issue?

````
The CORS settings are preventing the JavaScript from loading the file.
````

---

You need to provide customers with rich visualizations that allow you to easily connect multiple disparate data sources in S3, Redshift, and several CSV files. Which tool should you use that requires the least setup?

````
QuickSight
````

---

You work for a global marketing SaaS vendor that sells to content and marketing managers around the world so they can see analytics about their data. Your frontend development team is attempting to put together automated visualizations for your clients within their dashboards. What solution do you recommend they investigate?

````
Highcharts
````

---

Management has requested a comparison of total sales performance in the five North American regions in January. They're hoping to determine how to allocate budget to regions based on relative performance in that single period. What sort of visualization do you use in Amazon QuickSight?

````
A bar chart
````

---

You are using QuickSight to identify demand trends over multiple months for your top five product lines. Which type of visualization do you choose?

````
Line Chart
````

---

## Security

Your company stores very sensitive data on Redshift, which needs to be encrypted with keys that are fully controlled by your company. Which option should you use?

````
AWS CloudHSM

CloudHSM is a physical device that is attached to your VPC by AWS, and only you have access/control of the keys
````

---

A mobile application collects data that must be stored in multiple Availability Zones within five minutes of being captured in the app. How can you securely meet these requirements?

````
The mobile app should authenticate with an Amazon Cognito identity that is authorized to write to an Amazon Kinesis Firehose with an Amazon S3 destination.
````

---

What is the result of the following bucket policy?

````
{
    "Statement": [
        {
            "Sid": "Sid2",
            "Action": "s3:*",
            "Effect": "Allow",
            "Resource": "arn:aws:s3:::mybucket/*.",
            "Condition": {
                "ArnEquals": {
                    "s3:prefix": "data_team_"
                }
            },
            "Principal": {
                "AWS": [
                    "*"
                ]
            }
        }
    ]
}

It will allow all actions only against objects with the prefix data_team_ in the mybucket bucket.
````

---

Your application development team is building a solution with two applications. The security team wants each application's logs to be captured in two different places - because one of the applications produces logs with sensitive data. How can you meet the requirements with the least risk and effort?

````
 Use Amazon CloudWatch logs with two log groups, one for each application, and use an AWS IAM policy to control access to the log groups as required
````

---

You have an application with several hundred IoT devices all sending data into S3. Your team has created a mobile application that relies on reading data from DynamoDB. How could you give each mobile device permissions to read that data from DynamoDB?

````
Create an IAM role that can be assumed by an app that allows federated users.
````

---

What are the options to authenticate an IoT thing?

````
Amazon Cognito identities
IAM groups and roles
X.509 certificates
````

---

You need to alert your administrators every time downloads of specific objects in an S3 bucket occur. How do you do this?

````
Create a CloudTrail Trail that integrates with CloudWatch metrics and SNS to send alerts via SMS.
````

---

You are collecting large amounts of data from an application that is running on EC2 instances. This application processes sensitive information stored on S3. This data is accessed over the internet but your security team is concerned that the internet connectivity to Amazon S3 is a security risk. How could you mitigate this?

````
Access the data through a VPC endpoint for Amazon S3.

VPC endpoints for Amazon S3 provide secure connections to S3 buckets that do not require a gateway or NAT instances.
````

---

You've just deployed a Redshift cluster and are attempting to connect to it using Postico. You've already managed to connect to a separate Redshift cluster for another client that you're working with, but now you're unable to connect to this new cluster. What might be the issue?

````
You need to reconfigure your VPC to allow SSH traffic in on port 5439 from your IP.
````