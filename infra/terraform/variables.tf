variable "resource_group_name" {
  default = "open-data-ai-rg"
}
variable "location" {
  default = "Poland Central"
}
variable "vm_name" {
  default = "open-data-ai-vm"
}
variable "admin_username" {
  default = "azureuser"
}
variable "admin_password" {
  default   = "P@ssw0rd1234!"
  sensitive = true
}
variable "vm_size" {
  default = "Standard_B2s_v2"
}
variable "repo_url" {
  default = "https://github.com/maksym-hrytsyshyn/open-data-ai-analytics"
}
variable "web_port" {
  default = 5001
}
