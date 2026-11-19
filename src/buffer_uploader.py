import os
import json
import urllib.request
import subprocess

BUFFER_GRAPHQL_URL = "https://api.buffer.com/graphql"

def upload_release_asset(video_path: str, tag: str = "reels-v1") -> str:
    """
    Uploads video file to GitHub Releases using GitHub CLI or returns public URL.
    In GitHub Actions, GITHUB_TOKEN has write permission to publish releases.
    """
    repo = os.getenv("GITHUB_REPOSITORY", "satyamtiwarihindigaming-blip/gta6-cloud-clipper")
    filename = os.path.basename(video_path)
    
    print(f"[Buffer CDN] Uploading {filename} to GitHub Release {tag} on {repo}...")
    try:
        # Check if release exists; if not, create it
        cmd_create = ["gh", "release", "create", tag, video_path, "-R", repo, "--title", "Reels CDN Assets", "--notes", "Public CDN assets for Buffer"]
        res = subprocess.run(cmd_create, capture_output=True, text=True)
        if res.returncode != 0:
            # If already exists, upload asset with clobber
            cmd_upload = ["gh", "release", "upload", tag, video_path, "-R", repo, "--clobber"]
            res2 = subprocess.run(cmd_upload, capture_output=True, text=True)
            if res2.returncode != 0:
                print(f"[Buffer CDN] Release upload error: {res2.stderr}")
    except Exception as e:
        print(f"[Buffer CDN] Error running gh release: {e}")

    # Standard direct GitHub release asset download URL (redirects to AWS S3 / objects.githubusercontent.com)
    public_url = f"https://github.com/{repo}/releases/download/{tag}/{filename}"
    print(f"[Buffer CDN] Direct Asset URL: {public_url}")
    return public_url

def upload_reel_to_buffer(video_path: str, caption: str, channel_id: str = "6af8338e62b70b94b02aeee3") -> bool:
    """
    Publishes an Instagram Reel to Buffer using GraphQL API with direct GitHub Release CDN URL.
    """
    token = os.getenv("BUFFER_TOKEN")
    if not token:
        print("[Buffer] BUFFER_TOKEN secret not set. Skipping Instagram upload.")
        return False

    public_url = upload_release_asset(video_path)

    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess {
          post {
            id
            status
            dueAt
            channelService
          }
        }
        ... on InvalidInputError {
          message
        }
        ... on UnauthorizedError {
          message
        }
        ... on UnexpectedError {
          message
        }
      }
    }
    """

    variables = {
        "input": {
            "channelId": channel_id,
            "schedulingType": "automatic",
            "mode": "shareNow",
            "text": caption,
            "assets": [
                {
                    "video": {
                        "url": public_url
                    }
                }
            ],
            "metadata": {
                "instagram": {
                    "type": "reel",
                    "shouldShareToFeed": True
                }
            }
        }
    }

    req = urllib.request.Request(
        BUFFER_GRAPHQL_URL,
        data=json.dumps({"query": mutation, "variables": variables}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )

    try:
        print(f"[Buffer] Publishing Reel to Instagram (Channel ID: {channel_id})...")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            create_post = data.get("data", {}).get("createPost", {})
            post_obj = create_post.get("post")
            if post_obj:
                print(f"[Buffer] SUCCESS! Reel Queued/Published! Post ID: {post_obj.get('id')}, Status: {post_obj.get('status')}")
                return True
            else:
                err_msg = create_post.get("message") or data.get("errors")
                print(f"[Buffer] Error response: {err_msg}")
                return False
    except Exception as e:
        print(f"[Buffer] API Call failed: {e}")
        return False
