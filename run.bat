docker run -d ^
  -p 8000:8000 ^
  -v %cd%:/app ^
  --name pmp ^
  package-manager-python
