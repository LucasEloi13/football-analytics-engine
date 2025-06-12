#!/bin/bash

# Script de deploy com validação prévia para simular atomicidade
set -e  # Para na primeira falha

echo "🔍 Validando pré-requisitos..."

# Verificar tamanho das layers (se existirem)
if [ -f "layers/aws_dependencies/python.zip" ] && [ -f "layers/data_processing_dependencies/python.zip" ]; then
    echo "📏 Verificando tamanho das layers..."
    aws_size=$(unzip -l layers/aws_dependencies/python.zip | tail -1 | awk '{print $1}')
    data_size=$(unzip -l layers/data_processing_dependencies/python.zip | tail -1 | awk '{print $1}')
    total_size=$((aws_size + data_size))

    echo "Layer AWS: $(($aws_size / 1024 / 1024))MB"
    echo "Layer Data Processing: $(($data_size / 1024 / 1024))MB"
    echo "Total: $(($total_size / 1024 / 1024))MB"

    # Verificar se excede o limite (250MB = 262144000 bytes)
    if [ $total_size -gt 262144000 ]; then
        echo "❌ Erro: Tamanho total das layers ($((total_size / 1024 / 1024))MB) excede o limite de 250MB"
        echo "💡 Sugestão: Use 'requirements3.txt' que contém apenas as dependências essenciais"
        echo "💡 Execute: pip3 install --target terraform/layers/minimal/python -r requirements3.txt"
        exit 1
    fi
fi

# 1. Verificar se os arquivos necessários existem
if [ ! -f "layers/aws_dependencies/python.zip" ]; then
    echo "❌ Erro: layers/aws_dependencies/python.zip não encontrado"
    exit 1
fi

if [ ! -f "layers/data_processing_dependencies/python.zip" ]; then
    echo "❌ Erro: layers/data_processing_dependencies/python.zip não encontrado"
    exit 1
fi

if [ ! -f "lambdas/extract_competition_details_lambda/payload_files.zip" ]; then
    echo "❌ Erro: lambdas/extract_competition_details_lambda/payload_files.zip não encontrado"
    exit 1
fi

# 2. Verificar credenciais AWS
echo "🔐 Verificando credenciais AWS..."
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ Erro: Credenciais AWS não configuradas ou inválidas"
    exit 1
fi

# 3. Validar sintaxe do Terraform
echo "📋 Validando sintaxe do Terraform..."
if ! terraform validate; then
    echo "❌ Erro: Sintaxe do Terraform inválida"
    exit 1
fi

# 4. Fazer plan e verificar se não há erros
echo "📊 Executando terraform plan..."
if ! terraform plan -out=tfplan; then
    echo "❌ Erro: Terraform plan falhou"
    exit 1
fi

# 5. Aplicar apenas se tudo passou
echo "🚀 Aplicando mudanças..."
if terraform apply tfplan; then
    echo "✅ Deploy realizado com sucesso!"
    rm tfplan
else
    echo "❌ Erro: Deploy falhou"
    rm -f tfplan
    echo "🔄 Executando rollback..."
    terraform destroy -auto-approve
    exit 1
fi
