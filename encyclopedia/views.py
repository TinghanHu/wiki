from django.shortcuts import render, redirect 
from django.urls import reverse 
from . import util
import markdown2
from .forms import NewEntryForm
import random

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
                "message": f"Sorry, can't found the topic'{query}' 。",
                "title": "Not found"
            })
    # 如果不是 POST 請求，通常是直接訪問 /search，可以重定向到首頁或顯示錯誤
    return redirect(reverse("index"))

def new_page(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].strip()
            content = form.cleaned_data["content"].strip()

            # 檢查標題是否已存在 (不區分大小寫)
            if title.lower() in [e.lower() for e in util.list_entries()]:
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error_message": "Please choose the other topic。",
                    "title_page": "creat new page"
                })
            else:
                util.save_entry(title, content)
                return redirect(reverse("entry", args=[title]))
        else:
            # 如果表單無效，重新渲染表單並顯示錯誤
            return render(request, "encyclopedia/new_page.html", {
                "form": form,
                "title_page": "creat new page"
            })
    else:
        # 如果是 GET 請求，顯示一個空表單
        return render(request, "encyclopedia/new_page.html", {
            "form": NewEntryForm(),
            "title_page": "creat new page"
        })

def edit_page(request, title):
    # 檢查要編輯的條目是否存在
    entry_content = util.get_entry(title)
    if entry_content is None:
        # 如果條目不存在，顯示錯誤頁面
        return render(request, "encyclopedia/error.html", {
            "message": "Sorry, page not found.",
            "title": "page not found"
        })

    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"].strip()
            # 注意：這裡我們不允許編輯標題，因為 URL 已經指定了標題
            # 如果需要編輯標題，邏輯會更複雜，需要刪除舊檔案並創建新檔案

            util.save_entry(title, new_content) # 使用原標題保存新內容
            return redirect(reverse("entry", args=[title]))
        else:
            # 如果表單無效，重新渲染表單並顯示錯誤
            # 這裡我們需要重新填充標題和現有內容（因為錯誤可能在內容上）
            # 或者將錯誤訊息直接顯示
            return render(request, "encyclopedia/edit_page.html", {
                "title": title, # 傳遞當前條目的標題
                "form": form,
                "title_page": f"edit page：{title}"
            })
    else:
        # GET 請求：顯示預填充的表單
        # 使用 initial 參數來預填充表單字段
        form = NewEntryForm(initial={'title': title, 'content': entry_content})
        # 注意：在編輯模式下，我們通常會讓標題不可編輯，或者隱藏
        # 這裡我們依然傳遞 title 給模板，讓模板決定如何顯示
        # 在 forms.py 中的 NewEntryForm 裡，我們可以考慮讓 title 字段為只讀，或者在模板中控制
        return render(request, "encyclopedia/edit_page.html", {
            "title": title, # 傳遞當前條目的標題
            "form": form,
            "title_page": f"edit page：{title}"
        })
def random_page(request):
    all_entries = util.list_entries()
    if all_entries:
        random_entry = random.choice(all_entries) # 從所有條目中隨機選擇一個
        return redirect(reverse("entry", args=[random_entry])) # 重定向到該條目頁面
    else:
        # 如果沒有任何條目，可以重定向到首頁或顯示錯誤
        return render(request, "encyclopedia/error.html", {
            "message": "No topic to show",
            "title": "No topic"
        })    