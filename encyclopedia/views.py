from django.shortcuts import render, redirect 
from django.urls import reverse 
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return render(request, "encyclopedia/error.html",{ 
            "message": "Sorry, web not found.",
            "title": "web not found"})
    html_content = markdown2.markdown(entry_content)
    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST":
        query = request.POST.get("q").strip() # 獲取搜尋查詢並去除前後空白
        entries = util.list_entries()
        
        # 檢查是否完全匹配
        for entry_name in entries:
            if entry_name.lower() == query.lower():
                return redirect(reverse("entry", args=[entry_name])) # 重定向到完全匹配的條目頁面
        
        # 如果沒有完全匹配，則尋找包含子字串的條目
        matching_entries = [entry_name for entry_name in entries if query.lower() in entry_name.lower()]

        if matching_entries:
            # 如果有找到包含子字串的條目，顯示搜尋結果頁面
            return render(request, "encyclopedia/search_results.html", {
                "query": query,
                "entries": matching_entries
            })
        else:
            # 如果沒有找到任何匹配項
            return render(request, "encyclopedia/error.html", {
                "message": f"很抱歉，沒有找到與 '{query}' 相關的條目。",
                "title": "無搜尋結果"
            })
    # 如果不是 POST 請求，通常是直接訪問 /search，可以重定向到首頁或顯示錯誤
    return redirect(reverse("index"))




