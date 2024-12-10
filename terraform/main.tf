# terraform settings
terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = ">= 4.16"
        }
    }
    required_version = ">= 1.2.0"
}

# providers
provider aws {}

# resources
# resource "aws_instance" "webserver" {
#     # The first Linux AMI in the AMI catalog 
#     ami = "ami-0453ec754f44f9a4a"
#     instance_type = "t2.micro"
#     tags = {
#         name = "ExampleServer"
#     }
# }

# input


# output

