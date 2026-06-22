import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Import solve.py
sys.path.append(os.path.dirname(__file__))
from solve import verify_mosek

class TestMosekVerification(unittest.TestCase):
    @patch('solve.Expr')
    @patch('solve.Model')
    @patch('mosek.Env')
    @patch('os.path.exists')
    def test_verify_mosek_success(self, mock_exists, mock_mosek_env, mock_model, mock_expr):
        # Mocking Env.getversion
        mock_mosek_env.getversion.return_value = (10, 1, 0)
        
        # Mocking os.path.exists for license file
        mock_exists.return_value = True
        
        # Mock Model context manager and solve
        mock_model_instance = MagicMock()
        mock_model.return_value.__enter__.return_value = mock_model_instance
        
        # Mock variable level()
        mock_x = MagicMock()
        mock_x.level.return_value = [0.5, 0.5]
        mock_model_instance.variable.return_value = mock_x
        
        # We patch stdout to verify output
        with patch('sys.stdout') as mock_stdout:
            verify_mosek()
            # Check some print statements happened
            printed = [call.args[0] for call in mock_stdout.write.call_args_list if call.args]
            full_output = "".join(printed)
            self.assertIn("Verification solve result: x = 0.50, y = 0.50", full_output)
            self.assertIn("MOSEK license is successfully validated on this node!", full_output)

    @patch('solve.Model')
    @patch('mosek.Env')
    @patch('os.path.exists')
    @patch('sys.exit')
    def test_verify_mosek_license_failure(self, mock_exit, mock_exists, mock_mosek_env, mock_model):
        import mosek
        # Mocking Env.getversion
        mock_mosek_env.getversion.return_value = (10, 1, 0)
        
        # Mock Model to raise mosek.Error
        mock_model.side_effect = mosek.Error(mosek.rescode.err_missing_license_file, "Missing license file")
        
        # We patch stdout to verify output
        with patch('sys.stdout') as mock_stdout:
            verify_mosek()
            printed = [call.args[0] for call in mock_stdout.write.call_args_list if call.args]
            full_output = "".join(printed)
            self.assertIn("MOSEK error occurred", full_output)
            mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
