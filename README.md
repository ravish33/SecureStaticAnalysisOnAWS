# SecureStaticAnalysisOnAWS
A web service that securely analyze the given code using static analysis tool on AWS. The service is secure against SQL Injection, Buffer overflow, and Malicious inputs.  Passwords are also hashed to store them securely in database.
Follow this steps:
1. Create/Launch an EC2 instance on AWS.
-->   Select -->  Linux instance (free tier)

-->   Instance type: - t2.micro (free)

-->   IAM role:  Different roles to different user
        For example,
        for HR policies, we want to give read only access.  We cannot modify role.  To do so either add new role or create new instance.

-->   Add Storage Type

-->   Add Security Group: - To support inbound and out bound traffic.  HTTP, TCP/IP protocols allowance.
        For example, 
        We can assure a traffic inbound and out bound.  We can also restrict the network on the basis of protocols.

-->   Generate a key pair: 
        For example, key.pem 
        For windows we need .ppk file – to convert .pem to .ppk  use puttyKeyGen 
        For linux .pem file is supported.

2. Connect to EC2 instance:
-->   We used putty:-

        We can access the EC2 Instance using both the DNS name or IPv4.  
        We give the .ppk file as a password to access the EC2.
        
3. Develop the web service
-->   Download this repository and store it in EC2 instance.
-->   Remove the dependecies using commands in Linux Shell.
          pip install pymongo
          pip install flask
-->   Install RATS and FLOWFINDER in Linux Instance.  Follow the instructions in these links.
          Rats:
            https://security.web.cern.ch/security/recommendations/en/codetools/rats.shtml
          FlawFinder:
            https://security.web.cern.ch/security/recommendations/en/codetools/flawfinder.shtml
-->   Run the Python app.
