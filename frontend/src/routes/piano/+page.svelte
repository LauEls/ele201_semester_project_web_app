<script>
    import chartjs from 'chart.js/auto';
    import 'chartjs-adapter-moment';
    import { onMount } from 'svelte';

    let selectedDeviceName = $state('');
    let selectedMacAddress = $state('');
	let device_names = $state([]);
	let device_mac_addresses = $state([]);

    let timestamps = $state([]);
    let piano_mac_addresses = $state([]);
    let notes = $state([]);

    let pianoChartValues = [];
    let pianoCtx;
	let pianoChartCanvas;
	let pianoChart;

    onMount(async (promise) => {
        getData();

		pianoCtx = pianoChartCanvas.getContext('2d');
		pianoChart = new chartjs(pianoCtx, {
			type: 'line',
			data: {
					// labels: chartLabels,
					datasets: [{
							label: 'Piano Notes',
							backgroundColor: 'rgb(255, 99, 132)',
							borderColor: 'rgb(255, 99, 132)',
							data: pianoChartValues
					}]
			},
			options: {
				scales: {
					x: {
						type: 'time',
						time: {
							unit: 'second'
						}
					},
                    y: {
                        type: 'category',
                        labels: ['B', 'A', 'G', 'F', 'E', 'D', 'C']
                    }
				}
			}
		});

        const eventSource = new EventSource('http://localhost:8000/api/events/'); 
		// Listen for a specific event type (e.g., 'message')
		eventSource.addEventListener('piano-msg', function(event) {
            // 'event.data' will contain the data sent from the Django server
            const data = JSON.parse(event.data);
            console.log('Received message:', data.note.toUpperCase());
            notes.push(data.note);
			timestamps.push(data.timestamp);
			piano_mac_addresses.push(data.mac_address);
            
            if (data.mac_address.toLowerCase() == selectedMacAddress.toLowerCase()) {
				pianoChart.data.datasets[0].data.push({x: data.timestamp, y: data.note.toUpperCase()});
                pianoChart.update();
			}
		});

		// Listen for the 'open' event, which fires when the connection is established
		eventSource.onopen = function() {
		console.log('SSE connection opened.');
		};

		// Listen for the 'error' event, which fires if the connection encounters an error
		eventSource.onerror = function(error) {
		console.error('SSE error:', error);
		// Handle reconnection or display an error message
		};

		return () => eventSource.close();

	});

    async function  getData() {
		const device_endpoint = 'http://localhost:8000/api/registered-devices/'
		const solar_tracker_endpoint = 'http://localhost:8000/api/piano/'

		const [device_response, solar_tracker_response] = await Promise.all([
            fetch(device_endpoint),
            fetch(solar_tracker_endpoint)
        ]);

		if (!device_response.ok || !solar_tracker_response.ok) {
            throw new Error("Failed to fetch one or more endpoints");
        }

		const device_data = await device_response.json();
        const solar_tracker_data = await solar_tracker_response.json();

		device_names = [];
		device_mac_addresses = [];

		timestamps = [];
		piano_mac_addresses = [];
		notes = [];

		device_data.forEach(device => {
			device_names.push(device.device_name)
			device_mac_addresses.push(device.mac_address)
		});

		solar_tracker_data.forEach(datapoint => {
			notes.push(datapoint.note)
			timestamps.push(datapoint.timestamp)
			piano_mac_addresses.push(datapoint.mac_address)
		});

	}

    function handleChange(event) {
		selectedDeviceName = event.target.value;
        device_names.forEach((device_name, i) => {
			if (selectedDeviceName == device_name) {
				selectedMacAddress = device_mac_addresses[i];
			}
		});
        updateChart();
	}

    function updateChart() {
        // let mac_address = $state('');
		
		// chart.data.labels.length = 0;
		pianoChart.data.datasets[0].data.length = 0;
		// piano_mac_addresses.forEach((piano_mac_address, i) => {
		// 	if (piano_mac_address.toLowerCase() == selectedMacAddress.toLowerCase()) {
		// 		lightChart.data.datasets[0].data.push({x: timestamps[i], y: notes[i]});
        //         current_servo_angle = servo_angles[i];
		// 	}
		// });
		pianoChart.update();
    }

</script>

<div class="container">
    <h1>Piano</h1>
    <div class="form-floating">
		<select class="form-select" id="floatingSelect" aria-label="Floating label select example" onchange={handleChange}>
			<option selected>Select a device</option>
			{#each device_names as device_name}
				<option>{device_name}</option>
			{/each}
		</select>
		<label for="floatingSelect">Device Name</label> 
	</div>
	<canvas bind:this={pianoChartCanvas} id="piano_chart"></canvas>
</div>