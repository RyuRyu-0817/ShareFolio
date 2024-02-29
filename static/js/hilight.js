// ================================================================================
// 投稿情報(タイトルとカテゴリ)のキーワードに合致する部分をspanタグで囲んで、ハイライトする
//=================================================================================

let title_elements = document.getElementsByClassName("title-link");
let category_elements = document.getElementsByClassName("category-link");
title_elements = Array.from(title_elements);
category_elements = Array.from(category_elements);
search_elements = title_elements.concat(category_elements);

search_elements.forEach(search_element => {
    let search_element_text = search_element.textContent;
    keywords.forEach(keyword => {
        const pattern = new RegExp(keyword, "i");
        search_element_text = search_element_text.replace(
            pattern, 
            '<span class="hilight">' + keyword + '</span>'
        )
        search_element.innerHTML = search_element_text;
    });
})
