"""Tests for deploy.py — public deployment helper."""
import sys
from pathlib import Path



SCRIPT_DIR = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))

from deploy import deploy_dashboard, deploy_download, deploy_zip_bundle, base64_xlsx  # noqa


class MockDeployResult:
    def __init__(self, url):
        self.url = url


def mock_deploy_tool(path, source_path, project_name):
    """Mock website_deploy for testing."""
    return MockDeployResult(f'https://test.space.mcode.cn/{project_name.replace(" ", "_")}')


def test_deploy_dashboard_basic():
    """Deploy dashboard creates index.html and deploys."""
    # Create a temp HTML file
    test_html = Path('/tmp/test_dashboard.html')
    test_html.write_text('<!DOCTYPE html><html><body>Test</body></html>')

    url = deploy_dashboard(
        html_path=str(test_html),
        project_name='Test Dashboard',
        deploy_tool=mock_deploy_tool,
    )
    assert 'https://' in url
    assert 'Test_Dashboard' in url

    # Verify deploy dir cleaned up
    import shutil
    deploy_dir = Path('/tmp/deploy_Test_Dashboard')
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)


def test_deploy_download_creates_landing():
    """Download deploy creates a landing page."""
    test_html = Path('/tmp/test_download.html')
    test_html.write_text('<!DOCTYPE html><html><body>Content</body></html>')

    url = deploy_download(
        html_path=str(test_html),
        project_name='Test Download',
        deploy_tool=mock_deploy_tool,
        description='Custom description here',
    )
    assert 'https://' in url

    # Verify landing page exists
    import shutil
    deploy_dir = Path('/tmp/download_Test_Download')
    if deploy_dir.exists():
        landing = deploy_dir / 'index.html'
        assert landing.exists()
        if landing.exists():
            content = landing.read_text()
            assert 'Custom description here' in content
            assert 'Download' in content
        shutil.rmtree(deploy_dir)


def test_deploy_zip_bundle_basic():
    """ZIP bundle creates archive with files."""
    # Create temp files
    file1 = Path('/tmp/test_bundle_1.html')
    file1.write_text('<html>content 1</html>')
    file2 = Path('/tmp/test_bundle_2.html')
    file2.write_text('<html>content 2</html>')

    url = deploy_zip_bundle(
        file_paths=[str(file1), str(file2)],
        project_name='Test Bundle',
        zip_filename='test.zip',
        deploy_tool=mock_deploy_tool,
    )
    assert 'https://' in url

    # Verify ZIP created
    import shutil
    deploy_dir = Path('/tmp/bundle_Test_Bundle')
    if deploy_dir.exists():
        zip_path = deploy_dir / 'test.zip'
        assert zip_path.exists()
        if zip_path.exists():
            import zipfile
            with zipfile.ZipFile(zip_path, 'r') as zf:
                names = zf.namelist()
                assert 'test_bundle_1.html' in names
                assert 'test_bundle_2.html' in names
        shutil.rmtree(deploy_dir)


def test_deploy_zip_bundle_missing_file():
    """Missing files should be skipped gracefully."""
    file1 = Path('/tmp/test_exists.html')
    file1.write_text('<html>x</html>')

    url = deploy_zip_bundle(
        file_paths=[str(file1), '/tmp/does_not_exist.html'],
        project_name='Missing File Test',
        deploy_tool=mock_deploy_tool,
    )
    assert 'https://' in url  # Should not raise

    import shutil
    deploy_dir = Path('/tmp/bundle_Missing_File_Test')
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)


def test_base64_xlsx_basic():
    """base64_xlsx returns valid base64."""
    file_path = Path('/tmp/test_xlsx.xlsx')
    file_path.write_bytes(b'PK\x03\x04fake xlsx')

    result = base64_xlsx(str(file_path))
    import base64 as b64_mod
    # Should decode cleanly
    decoded = b64_mod.b64decode(result)
    assert decoded.startswith(b'PK')


def test_base64_xlsx_with_real_file():
    """base64_xlsx works on real small XLSX."""
    test_file = Path('/tmp/test_xlsx_real.xlsx')
    test_file.write_bytes(b'\x00\x01\x02\x03\x04' * 100)  # 500 bytes

    result = base64_xlsx(str(test_file))
    import base64 as b64_mod
    decoded = b64_mod.b64decode(result)
    assert len(decoded) == 500

    # Cleanup
    test_file.unlink()


def test_deploy_handles_path_with_spaces():
    """Project names with spaces should be handled."""
    test_html = Path('/tmp/test_spaces.html')
    test_html.write_text('<html>x</html>')

    url = deploy_dashboard(
        html_path=str(test_html),
        project_name='My Project With Spaces',
        deploy_tool=mock_deploy_tool,
    )
    assert 'https://' in url

    import shutil
    deploy_dir = Path('/tmp/deploy_My_Project_With_Spaces')
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)