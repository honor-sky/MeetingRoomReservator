const search_button = document.getElementById("search");
const button_section = document.getElementById("button-section");
const rooms_section = document.getElementById("rooms-section");
const main_content = document.getElementById("main-content");
const inputs = document.getElementsByTagName("input");
const required_inputs = document.getElementsByClassName("required");
const title = document.getElementById("title");

search_button.onclick = () => {
	var all_required = check_all_required();
	console.log(all_required);
	//index()

	if (all_required) {
		button_section.style.display = "none";
		title.innerText = "예약 정보";

		// for (i = 0; i < inputs.length; i++) {
		// 	inputs[i].setAttribute("disabled", true);
		// }

		main_content.style.justifyContent = "start";
		rooms_section.style.width = "700px";

		const rooms_title = document.createElement("div");
		rooms_title.setAttribute("id", "rooms-title");
		rooms_title.innerText = "현재 예약 가능한 회의실이에요";
		rooms_section.appendChild(rooms_title);

		load_rooms();
		reserve();
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

//백엔드에서 데이터 받아와서 사용할 부분
const load_rooms = () => {
	const room_area = document.createElement("div");
	room_area.setAttribute("class", "room-area");
	rooms_section.appendChild(room_area);

	const text_area = document.createElement("div");
	text_area.setAttribute("class", "text-area");

	const room_title = document.createElement("div");
	room_title.setAttribute("class", "room-title");

	const room_subtitle = document.createElement("div");
	room_subtitle.setAttribute("class", "room-subtitle");

	const room_name = document.createElement("span");
	room_name.setAttribute("class", "title-text");
	room_name.innerText = "도 회의실";

	const room_time = document.createElement("span");
	room_time.setAttribute("class", "title-text");
	room_time.innerText = " (13:00 ~ 15:00)";

	const room_location = document.createElement("span");
	room_location.setAttribute("class", "subtitle-text");
	room_location.innerText = "본사 1층,";

	const room_count = document.createElement("span");
	room_count.setAttribute("class", "subtitle-text");
	room_count.innerText = " 정원 8인";

	room_area.appendChild(text_area);

	text_area.appendChild(room_title);
	text_area.appendChild(room_subtitle);

	room_title.appendChild(room_name);
	room_title.appendChild(room_time);

	room_subtitle.appendChild(room_location);
	room_subtitle.appendChild(room_count);

	const button_area = document.createElement("div");
	button_area.setAttribute("class", "button-area");

	room_area.appendChild(button_area);

	const reserve_btn = document.createElement("button");
	reserve_btn.setAttribute("class", "main-button green reserve");
	reserve_btn.innerText = "예약";
	button_area.appendChild(reserve_btn);
};

const reserve = () => {
	const body = document.querySelector("body");
	const modal = document.querySelector(".modal");
	const reserve_btn = document.querySelector(".reserve");
	const reserve2_btn = document.querySelector(".reserve2");
	const want_time = document.getElementById("want-time").value;
	const start_time = document.getElementById("start-time");
	const end_time = document.getElementById("end-time");

	reserve_btn.addEventListener("click", () => {
		modal.classList.toggle("show");

		if (modal.classList.contains("show")) {
			body.style.overflow = "hidden";
		}
	});

	modal.addEventListener("click", (event) => {
		if (event.target === modal) {
			modal.classList.toggle("show");

			if (!modal.classList.contains("show")) {
				body.style.overflow = "auto";
			}
		}
	});

	if (want_time) {
		start_time.setAttribute("value", want_time);
		end_time.setAttribute("value", calculate_end_time());
	}

	start_time.addEventListener("change", () => {
		end_time.setAttribute("value", calculate_end_time());
	});

	reserve2_btn.addEventListener("click", () => {
		modal.style.display = "none";
		//데이터 보내기
		alert("예약이 완료 되었습니다.");
		location.reload();
	});
};

const calculate_end_time = () => {
	const start_time = document.getElementById("start-time");
	const how_time = document.getElementById("how-time").value;

	var end_hour_int =
		parseInt(start_time.value[0] + start_time.value[1]) + parseInt(how_time);
	var end_hour_str =
		"0" +
		end_hour_int.toString() +
		":" +
		start_time.value[3] +
		start_time.value[4];

	return end_hour_str;
};