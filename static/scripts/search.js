"use strict";
const API_BASE_URL = "/api";
let $gameSearch = $("#search_bar");
let currentPage = 1;
let currentTitle = "";
let currentPlatform = 0;
let info = $("#info_text");
let gameList = $("#game_list");
let content = $("#content-wrap");
let loadMore = document.createElement("button");
loadMore.textContent = "Load more";
$(loadMore).on("click", (e) =>
	getGames(currentTitle, currentPlatform, ++currentPage)
);

$gameSearch.on("submit", handleSubmission);

async function handleSubmission(e) {
	e.preventDefault();
	currentPage = 1;
	currentTitle = e.target[0].value;
	currentPlatform = parseInt(e.target[1].value);
	gameList.empty();
	getGames(currentTitle, currentPlatform, currentPage);
}

$(document).on("change", ".star-check", likeGame);

async function likeGame(e) {
	let $star = $(e.target);
	let checked = $star[0].checked;
	let game = $star.data();

	if (checked) {
		await axios.post(API_BASE_URL + `/like`, {
			game,
		});
	} else {
		await axios.post(API_BASE_URL + `/unlike`, {
			id: game.id,
		});
	}
}

async function getGames(title, platform, page) {
	info.text("Loading...");
	$(loadMore).detach();
	let response = await axios.post(API_BASE_URL + `/game/search`, {
		title,
		platform,
		page,
	});
	let games = response.data.game_list;
	let likes = response.data.likes;
	let last = response.data.last;
	if (games.length > 0) {
		info.text("");
		for (let game of games) {
			addGame(game, likes.includes(game.guid));
		}
		if (!last) $(content).append(loadMore);
	} else {
		info.text(
			"Sorry we couldnt find anything matching that. Try a different search."
		);
	}
}

function addGame(game, liked) {
	let li = document.createElement("li");
	li.className = "game_item";

	let img = document.createElement("img");
	if (game.image) {
		img.src = `${game.image.medium_url}`;
	} else {
		img.src = "static/images/pixel-mark.png";
	}
	img.alt = `${game.name} image`;
	img.className = "game_image";

	li.appendChild(img);

	let div = document.createElement("div");
	div.className = "info_wrap";
	let anchor = document.createElement("a");
	anchor.href = `/game/${game.guid}`;
	anchor.text = `${game.name}`;
	let p = document.createElement("p");
	p.innerText = `Description: ${game.deck}`;

	div.appendChild(anchor);
	div.appendChild(p);

	li.appendChild(div);

	let label = document.createElement("label");
	label.className = "star-wrap";
	let input = document.createElement("input");
	input.type = "checkbox";
	input.className = "star-check";
	if (liked) input.checked = true;
	$(input).data({
		id: game.guid,
		name: game.name,
		description: game.description,
		image_url: img.src,
		deck: game.deck,
	});
	let span = document.createElement("span");
	span.className = "star";

	label.appendChild(input);
	label.appendChild(span);

	li.appendChild(label);
	gameList.append(li);
}
