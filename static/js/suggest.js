
const list = categorys_obj.categorys;
// 入力が行われる要素
const elInput = document.querySelector("#id_category");
//　suggestされたカテゴリを表示するタグ
const elSuggestions = document.querySelector(".js-suggestions");
// 現在の値と入力されているかをみるフラグ
const state = {
    inputValue: elInput.value
};
const dataMap = new WeakMap();

function render() {
    renderInput();
    renderSuggestions();
}

// state.inputValueの値をフィールドにセット（空白もちゃんとやる）
function renderInput() {

    nowInputValue = elInput.value.split(" ").slice(0, -1).join(" ");
    if (nowInputValue != ""){
        elInput.value = nowInputValue + " " + state.inputValue + " ";
    }
    else{
        elInput.value = nowInputValue + state.inputValue + " ";

    }
    elInput.focus();
}
function renderSuggestions() {
    const elNewList = document.createElement("ul");
    elNewList.classList.add("category-list");
    // 最後の要素から検索
    target = elInput.value.split(" ").slice(-1)[0];
    if (target){
        // 正規表現のパターンを定義
        const start_pattern = new RegExp(`^${target}`, "i");
        const partial_pattern = new RegExp(target, "i");

        // 先頭文字での一致を先に実行
        start_filtered = list.filter(text => text.match(start_pattern))
        start_filtered.forEach(text => {
            const elItem = document.createElement("li");
            elItem.classList.add("category-item");
            dataMap.set(elItem, { text });
            elItem.textContent = text;
            elItem.addEventListener("click", handleClickItem);
            elNewList.appendChild(elItem);
        });
        // 先頭文字の後に部分一致検索を実行
        partial_filtered = list.filter(item => !start_filtered.includes(item)).filter(text => text.match(partial_pattern))
        partial_filtered.forEach(text => {
            const elItem = document.createElement("li");
            elItem.classList.add("category-item");
            dataMap.set(elItem, { text });
            elItem.textContent = text;
            elItem.addEventListener("click", handleClickItem);
            elNewList.appendChild(elItem);
        });
    }
    elSuggestions.innerHTML = "";
    elSuggestions.appendChild(elNewList);
}

// ハッシュマップにエレメントを格納
function handleClickItem(e) {
    state.inputValue = dataMap.get(e.currentTarget).text;
    render();
}

elInput.addEventListener("input", () => {
    state.inputValue = elInput.value;
    state.inputting = elInput.value !== "";

    renderSuggestions();
});
