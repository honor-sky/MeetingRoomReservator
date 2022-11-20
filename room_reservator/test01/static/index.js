const search_button = document.getElementById("search");
const required_inputs = document.getElementsByClassName("required");
const title = document.getElementById("title");

search_button.onclick = () => {
	var all_required = check_all_required();
	console.log(all_required);
	//index()

	if (all_required) {
		title.innerText = "예약 정보";
	} else {
		alert("모든 필수 요소를 입력해주세요");
	}
};

const check_all_required = () => {
	for (i = 0; i < required_inputs.length; i++) {
		if (required_inputs[i].value === "") {
			return false; //추후 수정
		}
	}
	return true;
};