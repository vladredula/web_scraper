## About Web Sraper
This project is to be used in [AWS Lambda](https://aws.amazon.com/lambda/). It scrapes the data from a source web page using [Beautiful Soup 4](https://beautiful-soup-4.readthedocs.io/en/latest/) and stores the data to [DynamoDB](https://aws.amazon.com/dynamodb/). It also creates the tables needed to store data into, if it does not exist.

#### Implementation
Clone the repo locally:
```
git clone https://github.com/vladredula/web_scraper.git webscraper
```
Navigate to `webscraper` folder. Select the following files/folders and make a zip file:
- `bs4 folder`
- `soupsieve folder`
- `lambda_function.py`
- `item.py`
- `category.py`
- `scraper.py`
> for `mac` select the items and right click and then choose compress
> for `windows` select the items and right click and then choose `Send to` > `Compressed (zipped)`

#### AWS Lambda
Here are the steps to make a lambda function:
- Go to [AWS Lambda](https://ap-northeast-1.console.aws.amazon.com/lambda/)
- Click the `Create Function` located on the upper right
- Select `Author from Scratch`
- You can type `webScraper` in the function name or anything you want
- Runtime: `Python 3.9`
- Click `Create function`

Attatch the policy below to your lambda excecution role:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:CreateTable",
                "dynamodb:BatchWriteItem",
                "dynamodb:DescribeTable",
                "dynamodb:ListTables"
            ],
            "Resource": "*"
        }
    ]
}
```

You can now upload the zip file that you create earlier.
- On your Lambda function, click on `Upload from` button located on the right side
- Click `Upload` and select the zip file you created and hit `Save`

We now need to add a reponse library as layer for the function to work.
- On your lamba function, click on the `Layers` located on the left panel and click `Create layer`
- Name: `Response`
- Select `Upload a .zip file` and click the `Upload` button
-- Navigate to the `webscaper` folder and choose the `request.zip` file
- Compatible architectures: `x86_64`
- Compatible runtimes: `Python 3.9`
- Click `Create`

After you created the layer, you need to add it to your Lambda function
- Navigate to your lambda function, scroll to down, and in the bottom click `Add a layer`
- Select `Custom layers`
- In the dropdown, select `Request` and in the version, select `1`
- Finally, click `Add`


##### Test
Now you can test the lambda function. 
- Click on `Test` button
- You can type anything in the `Event name` field
- You don't need to edit the event JSON since our lambda function doesn't need inputs so it will not matter.
- Click `Save`
- And click the `Test` button again to run the saved test

If the response is an `errorMessage` saying `Task timed out after 3.04 seconds`, you need to increase the `timeout` time to 1 minute. You can do so by:
- Go to the `Configuration` tab
- In the `General configuration`, click the `Edit` found at the right side corner.
- Scroll down and in the `Timeout` field, set it to 1 minute
- Hit `Save`

You can now test it again and the lambda function should be able to run smoothly now. The execution time should take about 52 seconds on the first run, since it needs to create tables to store data into.
Now, if you go to your DynamoDB, you should find the `items` and `categories` table. Inside these tables are the data scraped by the lambda function from the source web page