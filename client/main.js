const sendData = document.getElementById("send");
const display = document.getElementById("display");
let message;
let socket = io("http://192.168.0.243:5000", {
	extraHeaders: {
		clientType: "LIVETRACKER",
		orgId: "1233",
		deviceId: "319388df60723b99",
	},
});
let msgarray = JSON.parse(localStorage.getItem("msgarray")) || [];

socket.on("message", (message) => {
	console.log("Received private message:", message);
	display.innerText = message["data"];
});

socket.on("INITIAL", (message) => {
	console.log("message", message);
});

socket.on("LOCATION_TRACKING_UI", (message) => {
	console.log(typeof message);
	msgarray.push(
		`latitude: ${message["location"]["latitude"]} - longitude: ${message["location"]["longitude"]}`
	);
	localStorage.setItem("msgarray", JSON.stringify(msgarray));
	let data = "";
	msgarray.forEach((element) => {
		data = data + `<li>${element}</li>`;
	});
	console.log(data);
	display.innerHTML = data;
});

sendData.addEventListener("click", () => {
	message = document.getElementById("msg").value;
	socket.emit("message", { message });
});
