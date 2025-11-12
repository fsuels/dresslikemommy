document.addEventListener("DOMContentLoaded", function() {
    console.log("Size Conversion Script Loaded.");

    // Conversion Functions
    const cmToInches = cm => (cm / 2.54).toFixed(2);
    const kgToLbs = kg => (kg * 2.20462).toFixed(2);

    // Select Elements
    const sizeSelect = document.querySelector('select.size-select');
    const sizeChartWrapper = document.querySelector('.size-chart-wrapper');
    const sizeChartContent = document.getElementById('size-chart-content');

    // Error Handling for Missing Elements
    if (!sizeSelect) {
        console.error("Size dropdown not found.");
        return;
    } else {
        console.log("Size dropdown found.");
    }

    if (!sizeChartWrapper) {
        console.error("Size chart wrapper not found.");
        return;
    } else {
        console.log("Size chart wrapper found.");
    }

    /**
     * Parses the table headers to extract measurement names and units.
     * @param {HTMLCollection} headerCells - The header cells (th elements) of the table.
     * @returns {Object} - A mapping of column indices to measurement details.
     */
    const parseHeaders = (headerCells) => {
        const headerMap = {};
        for (let i = 0; i < headerCells.length; i++) {
            const headerText = headerCells[i].textContent.trim();
            const lowerHeader = headerText.toLowerCase();

            // Regular expression to extract measurement name and units
            const regex = /^(.+?)\s*\((.*?)\)$/;
            const match = headerText.match(regex);

            if (match) {
                let measurementName = match[1].trim(); // e.g., 'Bust'
                const unitsPart = match[2].trim(); // e.g., 'cm/in' or 'cm / in'
                const units = unitsPart.split('/').map(u => u.trim());

                // Correct measurement names if they have typos
                const lowerMeasurement = measurementName.toLowerCase();
                if (lowerMeasurement === 'bst') {
                    measurementName = 'Bust';
                }
                if (lowerMeasurement === 'wist') {
                    measurementName = 'Waist';
                }

                headerMap[i] = { name: measurementName, units: units };
            } else {
                // If no units are specified, assume 'cm'
                headerMap[i] = { name: headerText, units: ['cm'] };
            }
        }
        console.log("Parsed Headers:", headerMap);
        return headerMap;
    };

    /**
     * Retrieves size measurements from the size chart table.
     * @returns {Object} - An object mapping size names to their measurements.
     */
    const getFactorySizes = () => {
        console.log("Fetching size chart table...");
        const sizeChartTable = document.getElementById('size-chart');
        const factorySizes = {};

        if (sizeChartTable) {
            console.log("Size chart table found.");
            const rows = sizeChartTable.getElementsByTagName('tr');
            if (rows.length > 0) {
                const headerCells = rows[0].getElementsByTagName('th');
                if (headerCells.length > 0) {
                    const headerMap = parseHeaders(headerCells);
                    console.log("Header Map:", headerMap);

                    // Identify the 'Size' column index
                    let sizeIndex = -1;
                    for (let i = 0; i < headerCells.length; i++) {
                        if (headerMap[i].name.toLowerCase().includes('size')) {
                            sizeIndex = i;
                            break;
                        }
                    }

                    if (sizeIndex === -1) {
                        console.error("No 'Size' column found in size chart table.");
                        return factorySizes;
                    }

                    console.log(`'Size' column found at index ${sizeIndex}.`);

                    // Iterate through each data row
                    for (let i = 1; i < rows.length; i++) {
                        const cells = rows[i].getElementsByTagName('td');
                        if (cells.length === 0) continue;

                        const sizeName = cells[sizeIndex].textContent.trim();
                        if (!sizeName) {
                            console.warn(`Size name missing in row ${i + 1}.`);
                            continue;
                        }

                        factorySizes[sizeName] = {};

                        // Map each measurement based on headers
                        for (let j = 0; j < cells.length; j++) {
                            if (j === sizeIndex) continue; // Skip 'Size' column

                            const measurementInfo = headerMap[j];
                            if (!measurementInfo) {
                                console.warn(`No header mapping found for column ${j} in row ${i + 1}.`);
                                continue;
                            }

                            const measurementName = measurementInfo.name;
                            const units = measurementInfo.units;

                            const cellContent = cells[j].textContent.trim();

                            // Store measurement data
                            factorySizes[sizeName][measurementName] = {
                                value: cellContent,
                                units: units
                            };
                        }

                        // Debugging: Log the factory size measurements
                        console.log(`Factory Size for ${sizeName}:`, factorySizes[sizeName]);
                    }
                } else {
                    console.error("No header cells found in size chart table.");
                }
            } else {
                console.error("No rows found in size chart table.");
            }
        } else {
            console.error("Size chart table not found.");
        }
        console.log("Factory Sizes:", factorySizes);
        return factorySizes;
    };

    /**
     * Formats measurement values with appropriate units without duplication.
     * @param {string} value - The measurement value from the table.
     * @param {Array} units - The units associated with the measurement.
     * @returns {string} - The formatted measurement string.
     */
    function formatMeasurementWithUnits(value, units) {
        // Split the value by '/' to separate different units
        const parts = value.split('/').map(part => part.trim());

        if (parts.length === 2 && units.length === 2) {
            // Check if parts already contain units to prevent duplication
            const part0ContainsUnit = parts[0].toLowerCase().endsWith(units[0].toLowerCase());
            const part1ContainsUnit = parts[1].toLowerCase().endsWith(units[1].toLowerCase());

            const part0 = part0ContainsUnit ? parts[0] : `${parts[0]} ${units[0]}`;
            const part1 = part1ContainsUnit ? parts[1] : `${parts[1]} ${units[1]}`;

            return `${part0} / ${part1}`;
        } else if (parts.length === 1 && units.length === 1) {
            // Single unit provided (e.g., '88 cm')
            return parts[0];
        } else if (parts.length === 1 && units.length === 2) {
            // Assume the second unit is a conversion of the first
            const num = parseFloat(parts[0]);
            if (!isNaN(num)) {
                let convertedValue;
                if (units[1].toLowerCase() === 'in') {
                    convertedValue = cmToInches(num);
                } else if (units[1].toLowerCase() === 'lbs') {
                    convertedValue = kgToLbs(num);
                } else {
                    convertedValue = parts[0]; // No conversion available
                }
                return `${parts[0]} ${units[0]} / ${convertedValue} ${units[1]}`;
            } else {
                return `${value} ${units[0]}`;
            }
        } else {
            // Handle unexpected formats
            return value;
        }
    }

    /**
     * Updates the size chart wrapper with the selected size's measurements.
     */
    const updateSizeMessage = function() {
        const selectedSize = sizeSelect ? sizeSelect.value.trim() : null;
        console.log(`Selected Size: ${selectedSize}`);

        if (!selectedSize) {
            // Hide the size chart wrapper if no size is selected
            sizeChartWrapper.style.display = 'none';
            sizeChartContent.innerHTML = ''; // Clear any existing content
            console.log("Size chart hidden due to no selection.");
            return;
        }

        const factorySizes = getFactorySizes();

        // Match the selected size to the sizes in the factorySizes object
        let factorySize = factorySizes[selectedSize];
        console.log(`Factory Size Found:`, factorySize);

        if (!factorySize) {
            // Attempt to find a matching size ignoring case and whitespace
            for (let sizeName in factorySizes) {
                if (sizeName.replace(/\s+/g, '').toLowerCase() === selectedSize.replace(/\s+/g, '').toLowerCase()) {
                    factorySize = factorySizes[sizeName];
                    console.log(`Matched Size Ignoring Case/Whitespace: ${sizeName}`, factorySize);
                    break;
                }
            }
        }

        if (factorySize) {
            // Construct the size information HTML
            let htmlContent = `<p>Please review size details:</p>`;

            for (let measurementName in factorySize) {
                const measurementData = factorySize[measurementName];
                const units = measurementData.units;
                const value = measurementData.value;

                // Skip measurements with empty values
                if (!value || value.trim() === '') {
                    continue;
                }

                // Format the measurement value with units
                const formattedValue = formatMeasurementWithUnits(value, units);

                // Display the measurement
                htmlContent += `<p><strong>${measurementName}:</strong> ${formattedValue}</p>`;
            }

            // Insert the HTML into the size-chart-content div
            sizeChartContent.innerHTML = htmlContent;
            console.log("Size chart content updated:", htmlContent);

            // Show the size chart wrapper
            sizeChartWrapper.style.display = 'block';
            console.log("Size chart displayed.");
        } else {
            console.error("Selected size not found in factory sizes.");
            // Display an error message
            sizeChartContent.innerHTML = '<p>Size information not available.</p>';
            sizeChartWrapper.style.display = 'block';
            console.log("Size chart displayed with error message.");
        }
    };

    /**
     * Insert "Select size" as the first option in the size dropdown.
     */
    const insertSelectSizeOption = function() {
        if (sizeSelect) {
            // Check if the first option is already "Select size"
            const firstOption = sizeSelect.options[0];
            if (!firstOption || firstOption.value !== "") {
                // Create the "Select size" option
                const selectSizeOption = document.createElement('option');
                selectSizeOption.value = "";
                selectSizeOption.textContent = "Select size";
                selectSizeOption.disabled = true;
                selectSizeOption.selected = true;

                // Insert it at the beginning
                sizeSelect.insertBefore(selectSizeOption, sizeSelect.firstChild);
                console.log('"Select size" option inserted.');
            } else {
                console.log('"Select size" option already exists.');
            }
        }
    };

    /**
     * Reset the size select to default ("Select size") on page load.
     */
    const resetSizeSelect = function() {
        if (sizeSelect) {
            sizeSelect.value = ""; // Set to the default option with empty value
            // Trigger the update to hide the size chart initially
            updateSizeMessage();
            console.log("Size select reset to default.");
        }
    };

    // Insert "Select size" option before resetting the select
    insertSelectSizeOption();
    resetSizeSelect();

    // Event listener for size selection
    if (sizeSelect) {
        sizeSelect.addEventListener("change", updateSizeMessage);
        console.log("Change event listener added to size dropdown.");
    }
});
