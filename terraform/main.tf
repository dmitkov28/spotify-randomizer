
resource "spotify_playlist" "playlist" {
  name        = "Terraformed Playlist"
  description = "Created with Terraform"
  public      = false
  tracks      = jsondecode(data.external.script.result.track_ids)
}

data "external" "script" {
  program = ["uv", "run", "../src/main.py"]
}



