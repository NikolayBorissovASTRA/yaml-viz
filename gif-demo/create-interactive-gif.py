#!/usr/bin/env python3

import asyncio
import os
import subprocess
import sys
from pathlib import Path
from playwright.async_api import async_playwright

# Configuration settings - can be overridden via environment variables
CONFIG = {
    'gif_name': os.getenv('GIF_NAME', 'demo.gif'),
    'viewport_width': int(os.getenv('VIEWPORT_WIDTH', '800')),
    'viewport_height': int(os.getenv('VIEWPORT_HEIGHT', '1000')),
    'final_width': int(os.getenv('FINAL_WIDTH', '500')),
    'final_height': int(os.getenv('FINAL_HEIGHT', '650')),
    'fps': int(os.getenv('FPS', '6')),
    'max_colors': int(os.getenv('MAX_COLORS', '128')),
    'app_url': os.getenv('APP_URL', 'http://localhost:8501'),
    'template_file': os.getenv('TEMPLATE_FILE', 'pp.yml'),
    'project_name': os.getenv('PROJECT_NAME', 'Highway Construction Demo'),
    'slow_mo': int(os.getenv('SLOW_MO', '200')),
    'scene_pause': float(os.getenv('SCENE_PAUSE', '0.5')),
    'interaction_delay': float(os.getenv('INTERACTION_DELAY', '0.3')),
    'ultra_compress': os.getenv('ULTRA_COMPRESS', 'true').lower() == 'true',
    'ultra_width': int(os.getenv('ULTRA_WIDTH', '400')),
    'ultra_height': int(os.getenv('ULTRA_HEIGHT', '520')),
    'ultra_fps': int(os.getenv('ULTRA_FPS', '5')),
    'ultra_colors': int(os.getenv('ULTRA_COLORS', '64')),
    'size_limit_mb': float(os.getenv('SIZE_LIMIT_MB', '1.0'))
}

def print_config():
    """Print current configuration"""
    print("🔧 Demo Configuration:")
    print(f"   GIF Name: {CONFIG['gif_name']}")
    print(f"   Viewport: {CONFIG['viewport_width']}x{CONFIG['viewport_height']}")
    print(f"   Output: {CONFIG['final_width']}x{CONFIG['final_height']} @ {CONFIG['fps']}fps")
    print(f"   Colors: {CONFIG['max_colors']}")
    print(f"   Size Limit: {CONFIG['size_limit_mb']} MB")
    if CONFIG['ultra_compress']:
        print(f"   Ultra Compression: {CONFIG['ultra_width']}x{CONFIG['ultra_height']} @ {CONFIG['ultra_fps']}fps, {CONFIG['ultra_colors']} colors")

async def create_interactive_demo():
    """Create an interactive demo GIF with real form interactions"""
    
    print_config()
    
    async with async_playwright() as p:
        print("🎬 Starting interactive demo recording...")
        
        # Launch browser with video recording  
        browser = await p.chromium.launch(
            headless=False,  # Show browser for debugging
            slow_mo=CONFIG['slow_mo']  # Configurable action speed
        )
        
        # Create context with video recording - configurable resolution
        context = await browser.new_context(
            viewport={'width': CONFIG['viewport_width'], 'height': CONFIG['viewport_height']},
            record_video_dir='recordings/',
            record_video_size={'width': CONFIG['viewport_width'], 'height': CONFIG['viewport_height']}
        )
        
        page = await context.new_page()
        
        try:
            # Navigate to the app
            print("📱 Loading application...")
            await page.goto(CONFIG['app_url'])
            
            # Wait for app to load completely
            await page.wait_for_selector('h1:has-text("Dynamic YAML Form Generator")', timeout=30000)
            await asyncio.sleep(1)
            
            print(f"📝 Scene 1: Initial state ({CONFIG['scene_pause']}s)")
            await asyncio.sleep(CONFIG['scene_pause'])
            
            # Scene 2: Select template from dropdown (slower for visibility)
            print("📝 Scene 2: Selecting template...")
            
            # Find and click the selectbox - Streamlit uses a specific structure
            try:
                # Pause before clicking to show the empty state
                await asyncio.sleep(CONFIG['interaction_delay'])
                
                # Click on the selectbox to open dropdown
                selectbox = page.locator('div[data-testid="stSelectbox"]').first
                await selectbox.hover()  # Hover first to show we're about to click
                await asyncio.sleep(CONFIG['interaction_delay'])
                await selectbox.click()
                await asyncio.sleep(1)  # Wait longer to show dropdown is open
                
                # Wait for dropdown options to appear and select template
                # Streamlit creates a listbox with options
                option = page.locator('li[role="option"]').filter(has_text=CONFIG['template_file'])
                if await option.count() > 0:
                    await option.hover()  # Hover over the option first
                    await asyncio.sleep(CONFIG['interaction_delay'])
                    await option.click()
                    print(f"✅ Selected {CONFIG['template_file']} template")
                else:
                    # Try alternative approach - click second option
                    options = page.locator('li[role="option"]')
                    if await options.count() > 1:
                        await options.nth(1).hover()
                        await asyncio.sleep(CONFIG['interaction_delay'])
                        await options.nth(1).click()
                        print("✅ Selected template from list")
                
                await asyncio.sleep(CONFIG['interaction_delay'])  # Faster form appearance
                
            except Exception as e:
                print(f"⚠️ Template selection failed: {e}")
                # Try file upload as alternative
                print("Trying file upload instead...")
                file_input = page.locator('input[type="file"]')
                if await file_input.count() > 0:
                    await file_input.set_input_files(f'templates/{CONFIG["template_file"]}')
                    print(f"✅ Uploaded {CONFIG['template_file']} template")
                    await asyncio.sleep(1)
            
            # Scene 3: Fill in the form fields
            print("📝 Scene 3: Filling form fields...")
            
            # Wait for form to render
            await asyncio.sleep(1)
            
            # Fill text input if available
            text_inputs = page.locator('input[type="text"]')
            if await text_inputs.count() > 0:
                first_input = text_inputs.first
                await first_input.click()
                await first_input.fill("")  # Clear first
                await page.keyboard.type(CONFIG['project_name'], delay=50)
                print("✅ Filled project name")
                await asyncio.sleep(CONFIG['interaction_delay'])
            
            # Try to interact with MULTIPLE multiselects
            multiselects = page.locator('div[data-testid="stMultiSelect"]')
            if await multiselects.count() > 0:
                print(f"📝 Found {await multiselects.count()} multiselect fields...")
                
                # Interact with first multiselect
                first_multi = multiselects.first
                await first_multi.hover()
                await asyncio.sleep(CONFIG['interaction_delay'])
                await first_multi.click()
                await asyncio.sleep(CONFIG['interaction_delay'])
                
                # Select multiple options from first multiselect
                multi_options = page.locator('li[role="option"]')
                if await multi_options.count() > 0:
                    # Select first option
                    await multi_options.first.hover()
                    await asyncio.sleep(CONFIG['interaction_delay'])
                    await multi_options.first.click()
                    await asyncio.sleep(CONFIG['interaction_delay'])
                    
                    # Select second option
                    if await multi_options.count() > 1:
                        await multi_options.nth(1).hover()
                        await asyncio.sleep(CONFIG['interaction_delay'])
                        await multi_options.nth(1).click()
                        await asyncio.sleep(CONFIG['interaction_delay'])
                    
                    # Select third option if exists
                    if await multi_options.count() > 2:
                        await multi_options.nth(2).hover()
                        await asyncio.sleep(CONFIG['interaction_delay'])
                        await multi_options.nth(2).click()
                        await asyncio.sleep(CONFIG['interaction_delay'])
                    
                    print("✅ Selected multiple options from first multiselect")
                
                # Click outside to close dropdown
                await page.mouse.click(100, 100)
                await asyncio.sleep(CONFIG['interaction_delay'])
                
                # If there's a second multiselect, interact with it too
                if await multiselects.count() > 1:
                    print("📝 Interacting with second multiselect...")
                    second_multi = multiselects.nth(1)
                    await second_multi.hover()
                    await asyncio.sleep(CONFIG['interaction_delay'])
                    await second_multi.click()
                    await asyncio.sleep(CONFIG['interaction_delay'])
                    
                    # Select options from second multiselect
                    multi_options2 = page.locator('li[role="option"]')
                    if await multi_options2.count() > 0:
                        await multi_options2.first.hover()
                        await asyncio.sleep(CONFIG['interaction_delay'])
                        await multi_options2.first.click()
                        await asyncio.sleep(CONFIG['interaction_delay'])
                        
                        if await multi_options2.count() > 1:
                            await multi_options2.nth(1).hover()
                            await asyncio.sleep(CONFIG['interaction_delay'])
                            await multi_options2.nth(1).click()
                        
                        print("✅ Selected options from second multiselect")
                    
                    # Click outside to close
                    await page.mouse.click(100, 100)
                    await asyncio.sleep(CONFIG['interaction_delay'])
            
            # Scene 4: Navigate Inventargruppe tabs with specific selections
            print("📝 Scene 4: Inventargruppe tab navigation...")
            tabs = page.locator('button[role="tab"]')
            if await tabs.count() > 1:
                
                # Navigate to Orientierung (ORT) tab
                print("📝 Selecting items from Orientierung (ORT)...")
                ort_tab = tabs.filter(has_text="Orientierung")
                if await ort_tab.count() == 0:
                    # Fallback to first tab if text filter doesn't work
                    ort_tab = tabs.first
                
                await ort_tab.hover()
                await asyncio.sleep(CONFIG['interaction_delay'])
                await ort_tab.click()
                await asyncio.sleep(CONFIG['interaction_delay'])
                
                # Select specific items from Orientierung
                ort_multiselect = page.locator('div[data-testid="stMultiSelect"]').last
                if await ort_multiselect.count() > 0:
                    await ort_multiselect.click()
                    await asyncio.sleep(CONFIG['interaction_delay'])
                    
                    # Look for specific Orientierung options
                    referenz_option = page.locator('li[role="option"]').filter(has_text="Referenzpunkte")
                    rbbs_option = page.locator('li[role="option"]').filter(has_text="RBBS")
                    
                    if await referenz_option.count() > 0:
                        await referenz_option.hover()
                        await asyncio.sleep(CONFIG['interaction_delay'])
                        await referenz_option.click()
                        print("✅ Selected Referenzpunkte (REF)")
                        await asyncio.sleep(CONFIG['interaction_delay'])
                    
                    if await rbbs_option.count() > 0:
                        await rbbs_option.hover()
                        await asyncio.sleep(CONFIG['interaction_delay'])
                        await rbbs_option.click()
                        print("✅ Selected RBBS-Achse")
                        await asyncio.sleep(CONFIG['interaction_delay'])
                    
                    await page.mouse.click(100, 100)
                    await asyncio.sleep(CONFIG['interaction_delay'])
                
                # Navigate to Umgebung (UMG) tab
                print("📝 Selecting items from Umgebung (UMG)...")
                umg_tab = tabs.filter(has_text="Umgebung")
                if await umg_tab.count() == 0:
                    # Fallback to second tab if text filter doesn't work
                    umg_tab = tabs.nth(1) if await tabs.count() > 1 else tabs.first
                
                await umg_tab.hover()
                await asyncio.sleep(CONFIG['interaction_delay'])
                await umg_tab.click()
                await asyncio.sleep(CONFIG['interaction_delay'])
                
                # Select specific items from Umgebung
                umg_multiselect = page.locator('div[data-testid="stMultiSelect"]').last
                if await umg_multiselect.count() > 0:
                    await umg_multiselect.click()
                    await asyncio.sleep(CONFIG['interaction_delay'])
                    
                    # Look for specific Umgebung options
                    gelande_option = page.locator('li[role="option"]').filter(has_text="Geländemodell")
                    gebaude_option = page.locator('li[role="option"]').filter(has_text="Gebäude")
                    vermessung_option = page.locator('li[role="option"]').filter(has_text="Amtliche Vermessung")
                    
                    if await gelande_option.count() > 0:
                        await gelande_option.hover()
                        await asyncio.sleep(CONFIG['interaction_delay'])
                        await gelande_option.click()
                        print("✅ Selected Geländemodell (GLM)")
                        await asyncio.sleep(CONFIG['interaction_delay'])
                    
                    if await gebaude_option.count() > 0:
                        await gebaude_option.hover()
                        await asyncio.sleep(CONFIG['interaction_delay'])
                        await gebaude_option.click()
                        print("✅ Selected Gebäude (GEB)")
                        await asyncio.sleep(CONFIG['interaction_delay'])
                    
                    if await vermessung_option.count() > 0:
                        await vermessung_option.hover()
                        await asyncio.sleep(CONFIG['interaction_delay'])
                        await vermessung_option.click()
                        print("✅ Selected Amtliche Vermessung (AMV)")
                        await asyncio.sleep(CONFIG['interaction_delay'])
                    
                    await page.mouse.click(100, 100)
                    await asyncio.sleep(CONFIG['interaction_delay'])
                
                # Show a third tab briefly if it exists
                if await tabs.count() > 2:
                    third_tab = tabs.nth(2)
                    await third_tab.hover()
                    await asyncio.sleep(CONFIG['interaction_delay'])
                    await third_tab.click()
                    print("✅ Briefly showed third tab")
                    await asyncio.sleep(CONFIG['interaction_delay'])
                
                # Return to show the completed selections
                await umg_tab.hover()
                await asyncio.sleep(CONFIG['interaction_delay'])
                await umg_tab.click()
                print("✅ Returned to show Umgebung selections")
                await asyncio.sleep(CONFIG['interaction_delay'])
            
            # Scene 5: Show live preview
            print("📝 Scene 5: Live preview...")
            
            # Scroll to preview section
            preview_header = page.locator('h3:has-text("Live Preview")')
            if await preview_header.count() > 0:
                await preview_header.scroll_into_view_if_needed()
                print("✅ Showing live YAML preview")
                await asyncio.sleep(CONFIG['interaction_delay'])
            
            # Scene 6: Validate YAML
            print("📝 Scene 6: YAML validation...")
            
            validate_btn = page.locator('button:has-text("Validate YAML")')
            if await validate_btn.count() > 0:
                await validate_btn.click()
                print("✅ Clicked Validate YAML")
                await asyncio.sleep(1)
                
                # Check for success message
                success_msg = page.locator('.stSuccess')
                if await success_msg.count() > 0:
                    print("✅ YAML validation successful!")
            
            # Scene 7: Show download buttons
            print("📝 Scene 7: Export options...")
            
            download_yaml = page.locator('button:has-text("Download YAML")')
            if await download_yaml.count() > 0:
                await download_yaml.hover()
                print("✅ Hovering over Download YAML button")
                await asyncio.sleep(CONFIG['interaction_delay'])
            
            download_csv = page.locator('button:has-text("Download CSV")')
            if await download_csv.count() > 0:
                await download_csv.hover()
                print("✅ Hovering over Download CSV button")
                await asyncio.sleep(CONFIG['interaction_delay'])
            
            # Final pause
            await asyncio.sleep(1)
            
            print("✅ Interactive recording completed!")
            
        except Exception as e:
            print(f"❌ Error during recording: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await context.close()
            await browser.close()
    
    # Find the recorded video
    video_files = list(Path('recordings').glob('*.webm'))
    if not video_files:
        print("❌ No video file created")
        return False
    
    video_path = video_files[0]
    print(f"📹 Video saved: {video_path}")
    
    # Convert to GIF with optimization for smaller size
    print("🎞️ Converting to optimized GIF...")
    
    try:
        # Create optimized palette with configurable settings
        subprocess.run([
            'ffmpeg', '-y', '-i', str(video_path),
            '-vf', f'fps={CONFIG["fps"]},scale={CONFIG["final_width"]}:{CONFIG["final_height"]}:flags=lanczos,palettegen=max_colors={CONFIG["max_colors"]}:stats_mode=diff',
            'palette.png'
        ], check=True, capture_output=True)
        
        # Create compressed GIF with configurable settings
        subprocess.run([
            'ffmpeg', '-y',
            '-i', str(video_path),
            '-i', 'palette.png',
            '-lavfi', f'fps={CONFIG["fps"]},scale={CONFIG["final_width"]}:{CONFIG["final_height"]}:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle',
            '-loop', '0',
            CONFIG['gif_name']
        ], check=True, capture_output=True)
        
        print(f"✅ GIF created: {CONFIG['gif_name']}")
        
        # Check file size
        gif_size = Path(CONFIG['gif_name']).stat().st_size / (1024 * 1024)
        print(f"📊 Size: {gif_size:.2f} MB")
        
        if gif_size > CONFIG['size_limit_mb'] and CONFIG['ultra_compress']:
            print(f"⚠️ GIF >{CONFIG['size_limit_mb']}MB. Creating ultra-compressed version...")
            # Create even smaller version with configurable ultra settings
            subprocess.run([
                'ffmpeg', '-y', '-i', str(video_path),
                '-vf', f'fps={CONFIG["ultra_fps"]},scale={CONFIG["ultra_width"]}:{CONFIG["ultra_height"]}:flags=lanczos,palettegen=max_colors={CONFIG["ultra_colors"]}',
                'palette-small.png'
            ], check=True, capture_output=True)
            
            ultra_name = f'ultra-{CONFIG["gif_name"]}'
            subprocess.run([
                'ffmpeg', '-y',
                '-i', str(video_path),
                '-i', 'palette-small.png', 
                '-lavfi', f'fps={CONFIG["ultra_fps"]},scale={CONFIG["ultra_width"]}:{CONFIG["ultra_height"]}:flags=lanczos[x];[x][1:v]paletteuse=dither=none',
                '-loop', '0',
                ultra_name
            ], check=True, capture_output=True)
            
            small_size = Path(ultra_name).stat().st_size / (1024 * 1024)
            print(f"📊 Ultra compressed size: {small_size:.2f} MB")
            
            # Use the smaller version if it's under the limit
            if small_size <= CONFIG['size_limit_mb']:
                Path(CONFIG['gif_name']).unlink(missing_ok=True)
                Path(ultra_name).rename(CONFIG['gif_name'])
                print(f"✅ Using ultra-compressed version as {CONFIG['gif_name']}")
        
        # Cleanup
        Path('palette.png').unlink(missing_ok=True)
        Path('palette-small.png').unlink(missing_ok=True)
        for file in Path('recordings').glob('*'):
            file.unlink()
        Path('recordings').rmdir()
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg error: {e}")
        return False
    except FileNotFoundError:
        print("❌ FFmpeg not found. Install with: brew install ffmpeg")
        return False


if __name__ == "__main__":
    asyncio.run(create_interactive_demo())