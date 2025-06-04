# Variáveis de configuração principal
variable "aws_region" {
  description = "Região AWS onde os recursos serão criados"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nome do projeto - usado como prefixo para recursos"
  type        = string
  default     = "etl-data-pipeline"
}

variable "environment" {
  description = "Ambiente de deploy (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# Configurações dos buckets S3
variable "raw_data_bucket" {
  description = "Nome do bucket S3 para dados brutos"
  type        = string
  default     = "raw-data"
}

variable "processed_data_bucket" {
  description = "Nome do bucket S3 para dados processados"
  type        = string
  default     = "processed-data"
}

variable "lambda_code_bucket" {
  description = "Nome do bucket S3 para códigos das lambdas"
  type        = string
  default     = "lambda-code"
}

# Configurações das Lambdas
variable "lambda_runtime" {
  description = "Runtime das funções Lambda"
  type        = string
  default     = "python3.11"
}

variable "lambda_timeout" {
  description = "Timeout das funções Lambda em segundos"
  type        = number
  default     = 300
}

variable "lambda_memory_size" {
  description = "Tamanho da memória das funções Lambda em MB"
  type        = number
  default     = 1024
}

# Configurações das Layers
variable "python_layer_zip_path" {
  description = "Caminho para o arquivo ZIP da layer de dependências Python"
  type        = string
  default     = "layers/python.zip"
}

variable "etl_utilities_layer_zip_path" {
  description = "Caminho para o arquivo ZIP da layer de utilitários ETL"
  type        = string
  default     = "layers/etl_utilities.zip"
}

# Configurações das Lambdas de Extração
variable "extraction_lambdas" {
  description = "Configuração das lambdas de extração"
  type = map(object({
    name        = string
    description = string
    zip_path    = string
    handler     = string
  }))
  default = {
    "extraction_1" = {
      name        = "api-extraction-1"
      description = "Lambda para extração de dados da API 1"
      zip_path    = "lambda_packages/extraction_1.zip"
      handler     = "main.lambda_handler"
    }
    # "extraction_2" = {
    #   name        = "api-extraction-2"
    #   description = "Lambda para extração de dados da API 2"
    #   zip_path    = "lambda_packages/extraction_2.zip"
    #   handler     = "main.lambda_handler"
    # }
    # "extraction_3" = {
    #   name        = "api-extraction-3"
    #   description = "Lambda para extração de dados da API 3"
    #   zip_path    = "lambda_packages/extraction_3.zip"
    #   handler     = "main.lambda_handler"
    # }
    # "extraction_4" = {
    #   name        = "api-extraction-4"
    #   description = "Lambda para extração de dados da API 4"
    #   zip_path    = "lambda_packages/extraction_4.zip"
    #   handler     = "main.lambda_handler"
    # }
  }
}

# Configurações das Lambdas de Transformação
variable "transformation_lambdas" {
  description = "Configuração das lambdas de transformação"
  type = map(object({
    name        = string
    description = string
    zip_path    = string
    handler     = string
  }))
  default = {
    "transformation_1" = {
      name        = "data-transformation-1"
      description = "Lambda para transformação de dados 1"
      zip_path    = "lambda_packages/transformation_1.zip"
      handler     = "main.lambda_handler"
    }
    "transformation_2" = {
      name        = "data-transformation-2"
      description = "Lambda para transformação de dados 2"
      zip_path    = "lambda_packages/transformation_2.zip"
      handler     = "main.lambda_handler"
    }
    "transformation_3" = {
      name        = "data-transformation-3"
      description = "Lambda para transformação de dados 3"
      zip_path    = "lambda_packages/transformation_3.zip"
      handler     = "main.lambda_handler"
    }
    "transformation_4" = {
      name        = "data-transformation-4"
      description = "Lambda para transformação de dados 4"
      zip_path    = "lambda_packages/transformation_4.zip"
      handler     = "main.lambda_handler"
    }
  }
}

# Tags comuns para todos os recursos
variable "common_tags" {
  description = "Tags comuns aplicadas a todos os recursos"
  type        = map(string)
  default = {
    Project     = "ETL Data Pipeline"
    ManagedBy   = "Terraform"
    Environment = "dev"
  }
}