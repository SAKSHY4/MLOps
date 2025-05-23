storage "file" {
  path = "/home/binod/vault-data"
}
listener "tcp" {
  address = "127.0.0.1:8200"
  tls_disable = true
}
ui = true
