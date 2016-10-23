# Oauth Playground [DEMO](http://oauth.test.knnect.com/)
Playground application to show how OAuth works.
![oauth_playground_home](https://cloud.githubusercontent.com/assets/3313885/19464008/5104ea04-9516-11e6-85e0-3a1fc69cdab1.png)
This is a simple django web application for demonstrating OAuth authorization flow.You can simply try the [demo](http://oauth.test.knnect.com/)
Code in this repo is explained in this [article](http://me.knnect.com/blog/?p=344)

## How to run

If you interest in running the app locally, You have to install following dependencies
* Django
* Requests
* requests-oauthlib

Clone the repo and run `./manage.py runserver` to start the demo application.
To change the default OAuth parameters, Update the `oauth_playground/oauth_playground/configs.py` [configuration](https://github.com/tmkasun/oauth-playground/blob/master/oauth_playground/oauth_playground/configs.py) file accordingly and make sure you don't share this file.

### Configure to run with WSO2 APIM

You can use this playground application to try out the application developer experience using WSO2 APIM.
For example: If you want to consume an API which is managed by WSO2 APIM and to build an application. You can try out how to grant role based permissions to only allow specific users to access particular API
* Download the latest API Manager (APIM) pack from [wso2](http://wso2.com/products/api-manager/)
* Unzip , [run](https://docs.wso2.com/display/AM200/Running+the+Product) and login to APIM Publisher
* Create an API , and an application
* Use the generated Consumer keys and Consumer Secrete to try out the playground application
* You can use the API Console tool to try out the api invocation and get sample results. 

## Reference :
* [requests-oauthlib](http://requests-oauthlib.readthedocs.io/en/latest/examples/real_world_example.html)
* [Let'sEncrypt for SSL](https://www.digitalocean.com/community/tutorials/how-to-secure-apache-with-let-s-encrypt-on-ubuntu-16-04)

