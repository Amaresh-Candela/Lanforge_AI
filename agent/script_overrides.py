SCRIPT_OVERRIDES = {
    "lf_dataplane_test.py": {
        "required": [
            "upstream",
            "station",
            "dut",
            "traffic_types",
            "traffic_directions"
        ],
        "optional": [
            "speed",
            "duration",
            "spatial_streams",
            "bandwidths",
            "channels",
            "local_lf_report_dir",
            "verbosity"
        ]
    },
    "lf_wifi_capacity_test.py": {
        "required": [
            "upstream",
            "stations",
            "dut"
        ],
        "optional": [
            "duration",
            "spatial_streams",
            "bandwidths",
            "channels",
            "local_lf_report_dir",
            "verbosity"
        ]
    },
    "lf_wifi_capacity.py": {
        "required": [
            "upstream",
            "stations",
            "dut"
        ],
        "optional": [
            "duration",
            "spatial_streams",
            "bandwidths",
            "channels",
            "local_lf_report_dir",
            "verbosity"
        ]
    }
}
