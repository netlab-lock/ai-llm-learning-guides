#!/bin/bash
# scan_duplicates.sh - 扫描HTML文件中tip重复率
# 用法: bash scan_duplicates.sh <目录>
# 注意: 用sed提取中文，不用grep -oP！

DIR="${1:-.}"
total=0
problem=0

while IFS= read -r -d '' f; do
  total=$((total+1))
  n=$(grep -c 'class="tip"' "$f" 2>/dev/null)
  if [ "$n" -gt 1 ]; then
    tips=$(grep 'class="tip"' "$f" | sed 's/.*通俗类比[：:]//' | sed 's/<\/div>//' | cut -c1-60)
    u=$(echo "$tips" | sort -u | grep -c . 2>/dev/null)
    rate=$(( (n - u) * 100 / n ))
    if [ "$rate" -gt 20 ]; then
      problem=$((problem+1))
      echo "❌ $(basename "$f"): $n tips, $u unique, rate=${rate}%"
    fi
  fi
done < <(find "$DIR" -name "*.html" -print0 2>/dev/null)

echo ""
echo "Total: $total files, $problem problems, $(( (total-problem)*100/total ))% clean"
