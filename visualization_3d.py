"""
Three.js Advanced Visualization Dashboard Module for EchoWorld Nexus
Generates immersive 3D data exploration visualizations
"""

import json
from typing import Dict, Any, List
from datetime import datetime


def generate_threejs_globe_config(countries_data: List[Dict]) -> Dict[str, Any]:
    """
    Generate configuration for Three.js globe visualization
    
    Args:
        countries_data: List of country data with costs and coordinates
        
    Returns:
        Configuration object for Three.js visualization
    """
    
    country_coords = {
        "Germany": {"lat": 51.1657, "lng": 10.4515, "color": "#FFD700"},
        "Japan": {"lat": 36.2048, "lng": 138.2529, "color": "#FF4136"},
        "United States": {"lat": 37.0902, "lng": -95.7129, "color": "#0074D9"},
        "United Kingdom": {"lat": 55.3781, "lng": -3.4360, "color": "#B10DC9"},
        "Canada": {"lat": 56.1304, "lng": -106.3468, "color": "#FF851B"},
        "Australia": {"lat": -25.2744, "lng": 133.7751, "color": "#2ECC40"},
        "Netherlands": {"lat": 52.1326, "lng": 5.2913, "color": "#FF6600"},
        "Singapore": {"lat": 1.3521, "lng": 103.8198, "color": "#E91E63"},
        "France": {"lat": 46.2276, "lng": 2.2137, "color": "#001F3F"},
        "Spain": {"lat": 40.4637, "lng": -3.7492, "color": "#FFDC00"},
        "UAE": {"lat": 23.4241, "lng": 53.8478, "color": "#39CCCC"},
        "Portugal": {"lat": 39.3999, "lng": -8.2245, "color": "#01FF70"}
    }
    
    markers = []
    for country in countries_data:
        name = country.get("country", country.get("name", ""))
        if name in country_coords:
            coords = country_coords[name]
            markers.append({
                "country": name,
                "lat": coords["lat"],
                "lng": coords["lng"],
                "color": coords["color"],
                "cost_index": country.get("monthly_cost_eur", 2000),
                "ppp_index": country.get("ppp_index", 1.0),
                "avg_salary": country.get("avg_tech_salary", 5000)
            })
    
    return {
        "type": "globe",
        "markers": markers,
        "rotation_speed": 0.001,
        "marker_scale_factor": 0.0001,
        "camera_distance": 300,
        "ambient_light_intensity": 0.5,
        "point_light_intensity": 1.0
    }


def generate_threejs_cost_bars(countries_data: List[Dict]) -> Dict[str, Any]:
    """
    Generate 3D bar chart configuration for cost comparison
    
    Args:
        countries_data: List of country cost data
        
    Returns:
        Three.js 3D bar chart configuration
    """
    
    bars = []
    for i, country in enumerate(countries_data):
        bars.append({
            "id": f"bar_{i}",
            "label": country.get("country", "Unknown"),
            "value": country.get("monthly_cost_eur", 0),
            "height_scale": country.get("monthly_cost_eur", 2000) / 100,
            "position_x": i * 2,
            "color": generate_cost_color(country.get("monthly_cost_eur", 2000)),
            "metadata": {
                "currency": country.get("currency", "EUR"),
                "ppp_index": country.get("ppp_index", 1.0),
                "salary": country.get("avg_tech_salary", 0)
            }
        })
    
    return {
        "type": "bar_chart_3d",
        "bars": bars,
        "axis_labels": {
            "x": "Countries",
            "y": "Monthly Cost (EUR)",
            "z": "Relative Scale"
        },
        "animation": {
            "enabled": True,
            "duration": 1000,
            "easing": "easeOutCubic"
        },
        "interaction": {
            "hover_enabled": True,
            "click_enabled": True,
            "tooltip_enabled": True
        }
    }


def generate_threejs_savings_path(monte_carlo_results: Dict) -> Dict[str, Any]:
    """
    Generate 3D path visualization for Monte Carlo savings projections
    
    Args:
        monte_carlo_results: Monte Carlo simulation results
        
    Returns:
        Three.js 3D path visualization configuration
    """
    
    paths = []
    top_paths = monte_carlo_results.get("top_paths", [])
    
    colors = ["#48bb78", "#4299e1", "#ed8936", "#9f7aea", "#f56565"]
    
    for i, path in enumerate(top_paths[:5]):
        points = []
        monthly_savings = path.get("monthly_savings", 500)
        
        for month in range(13):
            points.append({
                "x": month,
                "y": monthly_savings * month + (monthly_savings * 0.1 * (month % 3)),
                "z": path.get("approval_prob", 0.75) * 10
            })
        
        paths.append({
            "id": f"path_{i}",
            "name": path.get("path_name", f"Path {i+1}"),
            "color": colors[i % len(colors)],
            "points": points,
            "probability": path.get("approval_prob", 0.75),
            "final_savings": path.get("total_savings_12m", 0),
            "line_width": 3 if i == 0 else 2
        })
    
    return {
        "type": "savings_paths_3d",
        "paths": paths,
        "axis_labels": {
            "x": "Months",
            "y": "Cumulative Savings (EUR)",
            "z": "Success Probability"
        },
        "grid": {
            "enabled": True,
            "divisions": 12
        },
        "target_line": {
            "enabled": True,
            "value": 11208,
            "label": "Visa Fund Target",
            "color": "#f56565"
        }
    }


def generate_threejs_vtc_flow(transactions: List[Dict]) -> Dict[str, Any]:
    """
    Generate 3D flow visualization for VTC transaction processing
    
    Args:
        transactions: List of VTC processed transactions
        
    Returns:
        Three.js 3D flow visualization configuration
    """
    
    nodes = []
    links = []
    
    source_node = {
        "id": "source",
        "type": "source",
        "label": "Incoming Transactions",
        "position": {"x": 0, "y": 0, "z": 0},
        "color": "#4299e1"
    }
    nodes.append(source_node)
    
    vtc_node = {
        "id": "vtc",
        "type": "processor",
        "label": "VTC Engine",
        "position": {"x": 50, "y": 0, "z": 0},
        "color": "#9f7aea"
    }
    nodes.append(vtc_node)
    
    approved_node = {
        "id": "approved",
        "type": "sink",
        "label": "Approved",
        "position": {"x": 100, "y": 25, "z": 0},
        "color": "#48bb78"
    }
    declined_node = {
        "id": "declined",
        "type": "sink",
        "label": "Declined",
        "position": {"x": 100, "y": -25, "z": 0},
        "color": "#f56565"
    }
    nodes.append(approved_node)
    nodes.append(declined_node)
    
    for i, tx in enumerate(transactions):
        amount = tx.get("amount", 0)
        status = tx.get("status", "Approved")
        
        links.append({
            "id": f"link_source_{i}",
            "source": "source",
            "target": "vtc",
            "value": amount,
            "category": tx.get("category", "other"),
            "animated": True
        })
        
        target = "approved" if status == "Approved" else "declined"
        links.append({
            "id": f"link_vtc_{i}",
            "source": "vtc",
            "target": target,
            "value": amount,
            "status": status,
            "animated": True,
            "delay": i * 200
        })
    
    return {
        "type": "flow_3d",
        "nodes": nodes,
        "links": links,
        "particle_system": {
            "enabled": True,
            "speed": 0.5,
            "size": 3
        },
        "camera": {
            "initial_position": {"x": 50, "y": 50, "z": 100},
            "look_at": {"x": 50, "y": 0, "z": 0}
        }
    }


def generate_threejs_dashboard_html(
    globe_config: Dict = None,
    bars_config: Dict = None,
    paths_config: Dict = None,
    flow_config: Dict = None
) -> str:
    """
    Generate complete Three.js dashboard HTML component
    
    Args:
        globe_config: Globe visualization config
        bars_config: Bar chart config
        paths_config: Savings paths config
        flow_config: VTC flow config
        
    Returns:
        HTML string with embedded Three.js visualization
    """
    
    configs = {
        "globe": globe_config or {},
        "bars": bars_config or {},
        "paths": paths_config or {},
        "flow": flow_config or {}
    }
    
    html = f"""
    <div id="threejs-dashboard" style="width: 100%; height: 600px; position: relative;">
        <div id="threejs-container" style="width: 100%; height: 100%;"></div>
        <div id="threejs-controls" style="position: absolute; top: 10px; right: 10px; z-index: 100;">
            <select id="viz-selector" style="padding: 8px; border-radius: 4px; background: #1a365d; color: white; border: 1px solid #4fd1c5;">
                <option value="globe">Global Cost Map</option>
                <option value="bars">Cost Comparison 3D</option>
                <option value="paths">Savings Projections</option>
                <option value="flow">VTC Transaction Flow</option>
            </select>
        </div>
        <div id="threejs-tooltip" style="position: absolute; display: none; padding: 10px; background: rgba(26, 54, 93, 0.95); color: white; border-radius: 8px; border: 1px solid #4fd1c5; font-size: 14px; pointer-events: none; z-index: 200;"></div>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    
    <script>
        const dashboardConfigs = {json.dumps(configs)};
        
        let scene, camera, renderer, controls;
        let currentVisualization = null;
        
        function initThreeJS() {{
            const container = document.getElementById('threejs-container');
            if (!container) return;
            
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x1a202c);
            
            camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.z = 150;
            
            renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);
            
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
            scene.add(ambientLight);
            
            const pointLight = new THREE.PointLight(0xffffff, 1);
            pointLight.position.set(50, 50, 50);
            scene.add(pointLight);
            
            loadVisualization('globe');
            animate();
        }}
        
        function loadVisualization(type) {{
            while(scene.children.length > 2) {{
                scene.remove(scene.children[scene.children.length - 1]);
            }}
            
            switch(type) {{
                case 'globe':
                    createGlobe(dashboardConfigs.globe);
                    break;
                case 'bars':
                    createBarChart(dashboardConfigs.bars);
                    break;
                case 'paths':
                    createSavingsPaths(dashboardConfigs.paths);
                    break;
                case 'flow':
                    createFlowVisualization(dashboardConfigs.flow);
                    break;
            }}
            currentVisualization = type;
        }}
        
        function createGlobe(config) {{
            const geometry = new THREE.SphereGeometry(50, 64, 64);
            const material = new THREE.MeshPhongMaterial({{
                color: 0x2d3748,
                transparent: true,
                opacity: 0.8,
                wireframe: false
            }});
            const globe = new THREE.Mesh(geometry, material);
            scene.add(globe);
            
            if (config.markers) {{
                config.markers.forEach(marker => {{
                    const phi = (90 - marker.lat) * (Math.PI / 180);
                    const theta = (marker.lng + 180) * (Math.PI / 180);
                    
                    const x = -50 * Math.sin(phi) * Math.cos(theta);
                    const y = 50 * Math.cos(phi);
                    const z = 50 * Math.sin(phi) * Math.sin(theta);
                    
                    const markerGeom = new THREE.SphereGeometry(2, 16, 16);
                    const markerMat = new THREE.MeshBasicMaterial({{ color: marker.color }});
                    const markerMesh = new THREE.Mesh(markerGeom, markerMat);
                    markerMesh.position.set(x, y, z);
                    markerMesh.userData = marker;
                    scene.add(markerMesh);
                }});
            }}
        }}
        
        function createBarChart(config) {{
            if (!config.bars) return;
            
            const spacing = 15;
            const startX = -(config.bars.length * spacing) / 2;
            
            config.bars.forEach((bar, i) => {{
                const height = bar.value / 50;
                const geometry = new THREE.BoxGeometry(10, height, 10);
                const material = new THREE.MeshPhongMaterial({{ color: bar.color }});
                const mesh = new THREE.Mesh(geometry, material);
                mesh.position.set(startX + i * spacing, height / 2, 0);
                mesh.userData = bar;
                scene.add(mesh);
            }});
            
            camera.position.set(0, 50, 100);
        }}
        
        function createSavingsPaths(config) {{
            if (!config.paths) return;
            
            config.paths.forEach(path => {{
                const points = path.points.map(p => new THREE.Vector3(p.x * 5, p.y / 100, p.z * 5));
                const curve = new THREE.CatmullRomCurve3(points);
                const geometry = new THREE.TubeGeometry(curve, 50, 0.5, 8, false);
                const material = new THREE.MeshPhongMaterial({{ color: path.color }});
                const mesh = new THREE.Mesh(geometry, material);
                scene.add(mesh);
            }});
            
            camera.position.set(50, 50, 100);
        }}
        
        function createFlowVisualization(config) {{
            if (!config.nodes) return;
            
            config.nodes.forEach(node => {{
                const geometry = new THREE.SphereGeometry(5, 32, 32);
                const material = new THREE.MeshPhongMaterial({{ color: node.color }});
                const mesh = new THREE.Mesh(geometry, material);
                mesh.position.set(node.position.x, node.position.y, node.position.z);
                mesh.userData = node;
                scene.add(mesh);
            }});
            
            camera.position.set(50, 30, 80);
        }}
        
        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        
        document.addEventListener('DOMContentLoaded', initThreeJS);
        
        const selector = document.getElementById('viz-selector');
        if (selector) {{
            selector.addEventListener('change', (e) => loadVisualization(e.target.value));
        }}
    </script>
    """
    
    return html


def generate_cost_color(cost: float) -> str:
    """Generate color based on cost level"""
    if cost < 1500:
        return "#48bb78"
    elif cost < 2500:
        return "#4299e1"
    elif cost < 3500:
        return "#ed8936"
    else:
        return "#f56565"


def get_visualization_for_streamlit(viz_type: str, data: Dict) -> Dict[str, Any]:
    """
    Get visualization configuration for Streamlit integration
    
    Args:
        viz_type: Type of visualization
        data: Data to visualize
        
    Returns:
        Visualization configuration and HTML
    """
    
    from data_module import compare_countries_cost, get_countries
    
    if viz_type == "globe":
        countries = get_countries()
        countries_data = compare_countries_cost(countries)
        config = generate_threejs_globe_config(countries_data)
        
    elif viz_type == "bars":
        countries = get_countries()
        countries_data = compare_countries_cost(countries)
        config = generate_threejs_cost_bars(countries_data)
        
    elif viz_type == "paths":
        config = generate_threejs_savings_path(data.get("monte_carlo", {}))
        
    elif viz_type == "flow":
        config = generate_threejs_vtc_flow(data.get("transactions", []))
        
    else:
        config = {}
    
    html = generate_threejs_dashboard_html(
        globe_config=config if viz_type == "globe" else None,
        bars_config=config if viz_type == "bars" else None,
        paths_config=config if viz_type == "paths" else None,
        flow_config=config if viz_type == "flow" else None
    )
    
    return {
        "type": viz_type,
        "config": config,
        "html": html
    }
