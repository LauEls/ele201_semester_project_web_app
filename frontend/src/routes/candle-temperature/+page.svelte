<script>
    import chartjs from 'chart.js/auto';
    import 'chartjs-adapter-moment';
    import { onMount } from 'svelte';

    let selectedDeviceName = $state('');
    let selectedMacAddress = $state('');
	let device_names = $state([]);
	let device_mac_addresses = $state([]);

    let timestamps = $state([]);
    let candle_mac_addresses = $state([]);
    let candle_lengths = $state([]);
    let elapsed_times = $state([]);

    let candleChartValues = [];
    let candleCtx;
	let candleChartCanvas;
	let candleChart;

    onMount(async (promise) => {
        getData();

		candleCtx = candleChartCanvas.getContext('2d');
		candleChart = new chartjs(candleCtx, {
			type: 'line',
			data: {
					// labels: chartLabels,
					datasets: [{
							label: 'Candle Length',
							backgroundColor: 'rgb(255, 99, 132)',
							borderColor: 'rgb(255, 99, 132)',
							data: candleChartValues
					}]
			},
			options: {
				scales: {
					x: {
						type: 'time',
						time: {
							unit: 'second'
						}
					}
				}
			}
		});

        const eventSource = new EventSource('http://localhost:8000/api/events/'); 
		// Listen for a specific event type (e.g., 'message')
		eventSource.addEventListener('candle-msg', function(event) {
            // 'event.data' will contain the data sent from the Django server
            const data = JSON.parse(event.data);
            console.log('Received message:', data);
            candle_lengths.push(data.candle_length);
            elapsed_times.push(data.elapsed_time);
			timestamps.push(data.timestamp);
			candle_mac_addresses.push(data.mac_address);
            
            if (data.mac_address.toLowerCase() == selectedMacAddress.toLowerCase()) {
				candleChart.data.datasets[0].data.push({x: data.elapsed_time, y: data.candle_length});
                candleChart.update();
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
		const solar_tracker_endpoint = 'http://localhost:8000/api/candle-length/'

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

		// timestamps = [];
		// car_mac_addresses = [];
		// notes = [];

		device_data.forEach(device => {
			device_names.push(device.device_name)
			device_mac_addresses.push(device.mac_address)
		});

		// solar_tracker_data.forEach(datapoint => {
		// 	notes.push(datapoint.note)
		// 	timestamps.push(datapoint.timestamp)
		// 	piano_mac_addresses.push(datapoint.mac_address)
		// });

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
		candleChart.data.datasets[0].data.length = 0;
		candleChart.update();
    }
</script>

<div class="container">
    <h1>Candle Temperature Measurement</h1>
    <div class="form-floating">
		<select class="form-select" id="floatingSelect" aria-label="Floating label select example" onchange={handleChange}>
			<option selected>Select a device</option>
			{#each device_names as device_name}
				<option>{device_name}</option>
			{/each}
		</select>
		<label for="floatingSelect">Device Name</label> 
	</div>
    <h2>Candle Length</h2>
    <canvas bind:this={candleChartCanvas} id="candle_chart"></canvas>
</div>