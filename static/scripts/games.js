"use strict";
const API_BASE_URL = "/api";
let $gameSearch = $("#search_bar");

$gameSearch.on("submit", handleSubmission);

async function handleSubmission(e) {
	// e.preventDefault();
}

$(document).on("change", ".star-check", likeGame);

async function likeGame(e) {
	let $star = $(e.target);
	let checked = $star[0].checked;
	console.log(checked);
	let li = $star.closest("li");
	let game = {
		id: li[0].dataset.id,
		name: li[0].children[1].children[0].text,
		description: li[0].dataset.desc,
		image_url: li[0].children[0].src,
		deck: li[0].children[1].children[1].textContent,
	};
	let response;
	if (checked) {
		let response = await axios.post(API_BASE_URL + `/like`, {
			game,
		});
	} else {
		let response = await axios.delete(API_BASE_URL + `/unlike`, {
			id: game.id,
		});
	}
	console.log(response);
}
