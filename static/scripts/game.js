const API_BASE_URL = "/api";

$(document).on("change", ".star-check", likeGame);

async function likeGame(e) {
	let $star = $(e.target);
	let checked = $star[0].checked;

	let game = {
		id: e.target.id,
	};

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
