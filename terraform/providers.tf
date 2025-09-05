terraform {
  required_version = "~> 1.13.1"
  required_providers {
    spotify = {
      version = "~> 0.2.7"
      source  = "conradludgate/spotify"
    }
    external = {
      source  = "hashicorp/external"
      version = "~> 2.3.5"
    }
  }

  backend "s3" {
    encrypt = true
  }
}

provider "spotify" {
  api_key = var.spotify_api_key
}
