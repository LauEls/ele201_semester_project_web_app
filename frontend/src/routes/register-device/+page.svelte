<script>
    let mac_address = $state('');
    let device_name = $state('');
    let form_state = $state(0);
    /** @type {HTMLFormElement | undefined} */
    let registerDeviceForm;
    
    async function handleSubmit() {
        'use strict'
        // event.preventDefault();

        if (registerDeviceForm) {
            registerDeviceForm.classList.add('was-validated');

            if (registerDeviceForm.checkValidity()) {
                try {
                    const endpoint = 'http://localhost:8000/api/registered-devices/'
                    let data = new FormData()
                    data.append('mac_address', mac_address)
                    data.append('device_name', device_name)
                    const response = await fetch(endpoint, {method: 'POST', body: data});

                    if (response.ok)
                    {
                        console.log("Success")
                        data = await response.json();
                        form_state = 2;
                        registerDeviceForm.reset();
                        registerDeviceForm.classList.remove('was-validated');

                    } else {
                        console.log("Fail")
                        form_state = 1;
                    }
                } catch (error) {
                    console.error('Error adding device name:', error);
                    form_state = 1;
                }
            }
        }

        
    }
</script>

<div class="container">
    <!-- <h1 style="text-align: center;">Register Device</h1> -->
    <h1>Register Device</h1>
    <form class="reister device needs-validation" bind:this={registerDeviceForm} onsubmit={handleSubmit} novalidate>
        <div class="form-floating mb-3">
            <input type="text" 
                class="form-control" 
                id="validationCustomMACAddress" 
                bind:value={mac_address} 
                required
                pattern={"^([0-9A-Fa-f]{2}-){5}([0-9A-Fa-f]{2})$"}
                placeholder="XX-XX-XX-XX-XX-XX"
            />
            <label for="validationCustomMACAddress" class="form-label">MAC Address</label>
            
            <div class="invalid-feedback">
                Please enter a MAC Address in the following format: XX-XX-XX-XX-XX-XX (where X is a hexadecimal digit)
            </div>
        </div>
        <div class="form-floating mb-3">
            <input type="text" 
                class="form-control" 
                id="input_device_name" 
                bind:value={device_name} 
                required
                placeholder="Device Name">
            <label for="input_device_name" class="form-label">Device Name</label>
            <div class="invalid-feedback">
                Please enter a device name
            </div>
        </div>

        {#if form_state==1}
            <div class="alert alert-danger" role="alert">
                Registering the device name failed!
            </div>
        {:else if form_state == 2}
            <div class="alert alert-success" role="alert">
                The device name was registered successfully!
            </div>
        {/if}

        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</div>

<!-- <style>
    .container {
        max-width: 500px;
    }
</style> -->