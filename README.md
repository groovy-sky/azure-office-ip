# TimerTrigger - Python

The `TimerTrigger` makes it incredibly easy to have your functions executed on a schedule. This sample demonstrates a simple use case of calling your function every 5 minutes.

## How it works

For a `TimerTrigger` to work, you provide a schedule in the form of a [cron expression](https://en.wikipedia.org/wiki/Cron#CRON_expression)(See the link for full details). A cron expression is a string with 6 separate expressions which represent a given schedule via patterns. The pattern we use to represent every 5 minutes is `0 */5 * * * *`. This, in plain text, means: "When seconds is equal to 0, minutes is divisible by 5, for any hour, day of the month, month, day of the week, or year".

## Learn more

<TODO> Documentation

https://office365azure.z6.web.core.windows.net/

# azure-office-ip

https://docs.microsoft.com/en-us/Office365/Enterprise/office-365-ip-web-service

https://endpoints.office.com/endpoints/worldwide?clientrequestid=b10c5ed1-bad1-445f-b386-b919946339a7

https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/storage

https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-static-website

https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-static-website-how-to?tabs=azure-portal

https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/storage/azure-storage-blob/azure/storage/blob/_blob_client.py

https://github.com/Azure/azure-functions-host/wiki/Retrieving-information-about-the-currently-running-function#python-on-functions-v2-or-higher

https://github.com/Azure/Azure-Functions/wiki/Bring-your-own-storage-(Linux-consumption)

https://www.serverlesslibrary.net/?technology=Functions%202.x&language=Python

https://github.com/yokawasa/azure-functions-python-samples

https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings#function_app_edit_mode