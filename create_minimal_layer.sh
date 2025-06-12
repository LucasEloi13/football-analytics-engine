#!/bin/bash

# Script para criar layer minimal usando requirements3.txt
set -e

echo "🏗️ Criando layer minimal com requirements3.txt..."

# Limpar diretório anterior se existir
rm -rf terraform/layers/minimal_dependencies

# Criar estrutura de diretórios
mkdir -p terraform/layers/minimal_dependencies/python

echo "📦 Instalando dependências essenciais..."
cd terraform/layers/minimal_dependencies

# Instalar dependências do requirements3.txt
pip3 install --target python/ -r ../../../requirements3.txt --no-deps

echo "🧹 Limpando arquivos desnecessários..."
# Remover arquivos desnecessários para reduzir tamanho
find python/ -name "*.pyc" -delete
find python/ -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find python/ -name "*.dist-info" -type d -exec rm -rf {} + 2>/dev/null || true
find python/ -name "tests" -type d -exec rm -rf {} + 2>/dev/null || true
find python/ -name "test_*" -delete 2>/dev/null || true

echo "📦 Compactando layer..."
zip -r python.zip python/ -x "*.pyc" "*/__pycache__/*" "*.dist-info/*"

echo "📊 Verificando tamanho da layer..."
echo "Tamanho compactado: $(du -h python.zip | cut -f1)"
echo "Tamanho descompactado: $(unzip -l python.zip | tail -1 | awk '{printf "%.1fMB", $1/1024/1024}')"

cd ../../..

echo "✅ Layer minimal criada em terraform/layers/minimal_dependencies/python.zip"
echo "💡 Para usar esta layer, atualize o terraform/lambda.tf para apontar para este arquivo"
