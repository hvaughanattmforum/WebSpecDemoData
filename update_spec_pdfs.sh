#!/bin/bash

SOURCE_DIR=$(pwd)
TARGET_BASE=~/Documents/GitHub/TMForum-ODA-Component-Specification/specifications

echo "🔁 Syncing GA PDFs into Component folders (replacing old ones)..."
echo "------------------------------------------------------------"

for source_pdf in "$SOURCE_DIR"/TMFC0*.pdf; do
  filename=$(basename "$source_pdf")

  # Extract component ID (e.g. TMFC001) and version
  comp_id=$(echo "$filename" | cut -d'_' -f1)
  version=$(echo "$filename" | sed -E 's/.*_v([0-9]+\.[0-9]+\.[0-9]+)\.pdf$/\1/')

  # Find target folder like TMFC001-ProductCatalogManagement
  target_folder=$(find "$TARGET_BASE" -type d -name "$comp_id-*" | head -n 1)

  if [[ -z "$target_folder" ]]; then
    echo "❌ No folder found for $comp_id — skipping"
    continue
  fi

  # Remove any existing TMFCxxx_*.pdf in the destination folder
  old_pdf=$(find "$target_folder" -maxdepth 1 -type f -name "${comp_id}_*.pdf" | head -n 1)
  if [[ -n "$old_pdf" ]]; then
    echo "🗑️  Removing old PDF: $(basename "$old_pdf")"
    rm -f "$old_pdf"
  fi

  # Copy the new GA PDF into the destination folder
  cp "$source_pdf" "$target_folder/$filename"
  echo "✅ $comp_id (v$version) copied to $target_folder"
done

echo "------------------------------------------------------------"
echo "✅ PDF sync and replacement complete."
