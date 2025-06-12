variable "aws_region"{
    type = string
    default = "us-east-2"
    
    validation {
        condition = contains(["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-west-1"], var.aws_region)
        error_message = "A região AWS deve ser uma das regiões suportadas."
    }
}

variable "bucket_name" {
    type = string
    
    validation {
        condition = length(var.bucket_name) > 3 && length(var.bucket_name) < 64
        error_message = "O nome do bucket deve ter entre 3 e 63 caracteres."
    }
    
    validation {
        condition = can(regex("^[a-z0-9][a-z0-9-]*[a-z0-9]$", var.bucket_name))
        error_message = "O nome do bucket deve conter apenas letras minúsculas, números e hífens."
    }
}