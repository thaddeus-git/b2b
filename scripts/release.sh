#!/bin/bash
# Usage: ./scripts/release.sh <version>
# Example: ./scripts/release.sh 1.4.5

VERSION=$1

if [ -z "$VERSION" ]; then
  echo "Usage: ./scripts/release.sh <version>"
  echo "Example: ./scripts/release.sh 1.4.5"
  exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
  echo "Error: You have uncommitted changes. Please commit or stash them first."
  exit 1
fi

echo "Releasing version $VERSION..."

# Update plugin.json version
sed -i '' "s/\"version\": \"[^\"]*\"/\"version\": \"$VERSION\"/" .claude-plugin/plugin.json

# Commit and tag
git add .claude-plugin/plugin.json
git commit -m "chore: bump version to $VERSION"
git tag -a "v$VERSION" -m "Release v$VERSION"
git push origin main
git push origin "v$VERSION"

# Create GitHub release
gh release create "v$VERSION" --title "v$VERSION" --generate-notes

echo "Released v$VERSION successfully!"
