# Feature Development Demo - NTP Configuration

This directory contains a complete, working example of how to add a new feature to WebZFS. The example implements NTP (Network Time Protocol) configuration management that works on both Linux and FreeBSD.

## What's Included

This demo provides:

1. **Complete Working Example** - A fully functional NTP configuration feature
2. **Comprehensive Guide** - Step-by-step instructions in `ADDING_NEW_FEATURES.md`
3. **All Three Layers** - Service, View, and Template implementations
4. **Best Practices** - OS compatibility, error handling, security patterns

## Directory Structure

```
add_feature_demo/
├── README.md                           # This file - overview
├── ADDING_NEW_FEATURES.md             # Complete developer guide
├── services/
│   └── ntp.py                          # Service layer - business logic
├── views/
│   └── utils_ntp.py                    # View layer - HTTP routing
└── templates/
    └── utils/
        └── ntp/
            ├── index.jinja             # Main page template
            ├── config.jinja            # Configuration editor template
            └── status_partial.jinja    # HTMX partial template
```

## Quick Start

To implement this NTP feature in your application:

### 1. Copy Files to Production Locations

```bash
# From the project root directory

# Copy service
cp add_feature_demo/services/ntp.py services/

# Copy view
cp add_feature_demo/views/utils_ntp.py views/

# Copy templates
cp -r add_feature_demo/templates/utils/ntp templates/utils/
```

### 2. Register the Router

Edit `views/__init__.py`:

```python
# Add import
import views.utils_ntp

# Add router registration (in the Utilities Routes section)
router.include_router(views.utils_ntp.router)
```

### 3. Add Navigation (Optional)

Edit `config/templates.py`, find the utilities section and add:

```python
{"label": "NTP Config", "url": "/utils/ntp"},
```

### 4. Add Sudo Permissions

Create `/etc/sudoers.d/webzfs-ntp`:

```
# NTP Management
webzfs ALL=(ALL) NOPASSWD: /bin/systemctl restart ntpd
webzfs ALL=(ALL) NOPASSWD: /bin/systemctl enable ntpd
webzfs ALL=(ALL) NOPASSWD: /bin/systemctl status ntpd
webzfs ALL=(ALL) NOPASSWD: /usr/sbin/service ntpd restart
webzfs ALL=(ALL) NOPASSWD: /usr/sbin/service ntpd status
webzfs ALL=(ALL) NOPASSWD: /usr/sbin/sysrc ntpd_enable=YES
webzfs ALL=(ALL) NOPASSWD: /bin/cp /tmp/ntp.conf.tmp /etc/ntp.conf
```

Set correct permissions:
```bash
sudo chmod 0440 /etc/sudoers.d/webzfs-ntp
```

### 5. Restart Application

```bash
./run.sh restart
```

### 6. Access the Feature

Navigate to: `http://your-server:26619/utils/ntp`

## Learning Path

### For Quick Understanding

1. Read the architecture overview in `ADDING_NEW_FEATURES.md`
2. Review `services/ntp.py` to see OS-specific handling
3. Look at `views/utils_ntp.py` to understand routing
4. Examine templates to see UI patterns

### For Deep Understanding

Work through `ADDING_NEW_FEATURES.md` completely - it covers:

- Architecture and design patterns
- Step-by-step implementation
- Testing strategies
- Security best practices
- Common pitfalls and solutions

## Key Concepts

### 1. OS Compatibility (Linux & FreeBSD)

```python
def _detect_os(self) -> str:
    """Detect operating system - defaults to Linux"""
    system = platform.system().lower()
    if 'freebsd' in system:
        return 'freebsd'
    else:
        # Default to Linux - handles all Linux distributions
        return 'linux'
```

### 2. Service Pattern

```python
class NTPService:
    """Handles logic and system operations"""
    
    def get_status(self) -> Dict:
        """Get current state"""
        pass
    
    def update_config(self, config: str) -> bool:
        """Modify configuration"""
        pass
```

### 3. FastAPI Routing

```python
@router.get("/")
async def index(request: Request):
    """Display main page"""
    data = service.get_data()
    return templates.TemplateResponse("template.jinja", {"data": data})

@router.post("/action")
async def action(request: Request, param: Annotated[str, Form()]):
    """Handle form submission"""
    result = service.do_action(param)
    return RedirectResponse(url="/?message=Success", status_code=303)
```

### 4. HTMX Integration

```jinja
<button hx-get="/utils/ntp/status/refresh" 
        hx-target="#status-container"
        hx-swap="innerHTML">
    Refresh Status
</button>
```

### 5. Dark Mode Support

```jinja
<div class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
    Content
</div>
```

## File Descriptions

### services/ntp.py (Service Layer)

**Purpose**: Logic and system operations

**Key Features**:
- OS detection (Linux/FreeBSD)
- NTP service management (start/stop/restart/enable)
- Configuration file handling
- Time synchronization status
- Error handling and validation

**Methods**:
- `get_status()` - Check if NTP service is running
- `get_config()` - Read configuration file
- `get_servers()` - Extract NTP servers from config
- `update_config()` - Write new configuration
- `restart_service()` - Restart NTP daemon
- `enable_service()` - Enable service at boot
- `get_time_info()` - Get current time and sync status

### views/utils_ntp.py (View Layer)

**Purpose**: HTTP routing and request handling

**Routes**:
- `GET /utils/ntp` - Main overview page
- `GET /utils/ntp/config` - Configuration editor
- `POST /utils/ntp/config/save` - Save configuration
- `POST /utils/ntp/service/restart` - Restart service
- `POST /utils/ntp/service/enable` - Enable at boot
- `GET /utils/ntp/status/refresh` - HTMX status refresh

**Patterns**:
- Authentication required for all routes
- POST-Redirect-GET pattern for form submissions
- Exception handling with user-friendly errors
- Query parameters for success/error messages

### templates/utils/ntp/*.jinja (Template Layer)

**index.jinja** - Main overview page with:
- Service status card
- NTP servers list
- Action buttons
- HTMX dynamic updates

**config.jinja** - Configuration editor with:
- Textarea for config file
- Save/Cancel buttons
- Help section with common directives
- Confirmation dialogs

**status_partial.jinja** - HTMX partial for:
- Dynamic status updates
- Service information
- System time display
- Sync status details

## Customizing for Your Feature

To adapt this example for your own feature:

1. **Replace NTP-specific logic** with your feature's logic
2. **Update route paths** from `/utils/ntp` to `/utils/your-feature`
3. **Modify templates** to display your data
4. **Adjust service methods** for your use case
5. **Update sudo permissions** as needed

## Testing the Demo

Even without installing, you can learn by examining:

1. **Code flow**: Follow a request from view → service → system command
2. **Error handling**: See how exceptions are caught and displayed
3. **OS differences**: Compare Linux vs FreeBSD command execution
4. **Template patterns**: Study the UI components and styling
5. **Security**: Review input validation and sudo usage

## Common Questions

**Q: Do I need to implement all these features?**
A: No, start simple. You can have just one page with basic functionality.

**Q: Can I skip the service layer?**
A: Not recommended. The service layer makes code testable and reusable.

**Q: What if my feature only works on Linux?**
A: That's fine! Just add a check and display an error on FreeBSD.

**Q: Should every feature have HTMX?**
A: No, only if you need dynamic updates without page refresh.

## Additional Resources

- **Full Guide**: Read `ADDING_NEW_FEATURES.md` for complete documentation
- **Existing Features**: Study `views/utils_smart.py` for a complex real-world example
- **Templates**: Look at `templates/zfs/` for advanced UI patterns
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Jinja2 Docs**: https://jinja.palletsprojects.com/
- **HTMX Docs**: https://htmx.org/

## Need Help?

1. Check existing features for similar patterns
2. Read the comprehensive guide in `ADDING_NEW_FEATURES.md`
3. Review error messages carefully
4. Test individual components separately
5. Ask in project discussions

## Next Steps

1. **Study this example** - Understand each layer and how they connect
2. **Read the full guide** - Work through `ADDING_NEW_FEATURES.md`
3. **Start small** - Begin with a simple feature (single page, basic functionality)
4. **Iterate** - Add complexity as needed (multiple pages, HTMX, etc.)
5. **Test thoroughly** - Both OSes, dark mode, error cases
6. **Document** - Help others understand your feature

---

Happy feature development! 🚀
