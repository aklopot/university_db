import json
import pytest
from unittest.mock import mock_open, patch, Mock
from src.models.universitydb import Gender
from src.repositories.repository_factories.database.json.json_gender_repository import JSONGenderRepository

@pytest.fixture
def repository():
    return JSONGenderRepository("test_genders.json")

@pytest.fixture
def sample_genders():
    return {
        'genders': [
            {'gender_id': 1, 'gender_name': "Mężczyzna"},
            {'gender_id': 2, 'gender_name': "Kobieta"}
        ]
    }

@pytest.fixture
def sample_gender():
    return Gender(gender_id=1, gender_name="Mężczyzna")

def test_load_data_existing_file(repository, sample_genders):
    # Arrange
    mock_file = mock_open(read_data=json.dumps(sample_genders))

    # Act
    with patch('builtins.open', mock_file):
        result = repository._load_data()

    # Assert
    assert len(result) == 2
    assert result[0].gender_id == 1
    assert result[0].gender_name == "Mężczyzna"
    assert result[1].gender_id == 2
    assert result[1].gender_name == "Kobieta"

def test_load_data_file_not_found(repository):
    # Arrange
    mock_read = mock_open()
    mock_read.side_effect = FileNotFoundError()
    mock_write = mock_open()
    mock_write.return_value.write.return_value = None
    
    # Act & Assert
    with patch('builtins.open', create=True) as mock_open_:
        mock_open_.side_effect = [
            FileNotFoundError(),  # Pierwszy odczyt
            mock_write.return_value,  # Pierwszy zapis
            mock_read.return_value  # Drugi odczyt
        ]
        mock_read.return_value.read.return_value = json.dumps({
            'genders': [
                {'gender_id': 1, 'gender_name': "Mężczyzna"},
                {'gender_id': 2, 'gender_name': "Kobieta"}
            ]
        })
        
        result = repository._load_data()
        
        assert len(result) == 2
        assert result[0].gender_name == "Mężczyzna"
        assert result[1].gender_name == "Kobieta"

def test_add_gender(repository, sample_genders):
    # Arrange
    mock_read = mock_open(read_data=json.dumps(sample_genders))
    mock_write = mock_open()
    combined_mock = Mock()
    combined_mock.side_effect = [mock_read.return_value, mock_write.return_value]

    new_gender = Gender(gender_name="Inne")

    # Act
    with patch('builtins.open', combined_mock):
        repository.add_gender(new_gender)

    # Assert
    write_calls = combined_mock.call_args_list
    assert len(write_calls) == 2  # read + write
    assert write_calls[1][0][1] == 'w'  # drugi call powinien być write

def test_update_gender(repository, sample_genders):
    # Arrange
    mock_read = mock_open(read_data=json.dumps(sample_genders))
    mock_write = mock_open()
    combined_mock = Mock()
    combined_mock.side_effect = [mock_read.return_value, mock_write.return_value]
    
    updated_gender = Gender(gender_id=1, gender_name="Mężczyzna (zaktualizowane)")

    # Act
    with patch('builtins.open', combined_mock):
        repository.update_gender(updated_gender)

    # Assert
    write_calls = combined_mock.call_args_list
    assert len(write_calls) == 2
    assert write_calls[1][0][1] == 'w'

def test_get_gender_by_name(repository, sample_genders):
    # Arrange
    mock_file = mock_open(read_data=json.dumps(sample_genders))

    # Act
    with patch('builtins.open', mock_file):
        result = repository.get_gender_by_name("Mężczyzna")

    # Assert
    assert result is not None
    assert result.gender_name == "Mężczyzna"
    assert result.gender_id == 1

def test_get_gender_by_name_not_found(repository, sample_genders):
    # Arrange
    mock_file = mock_open(read_data=json.dumps(sample_genders))

    # Act
    with patch('builtins.open', mock_file):
        result = repository.get_gender_by_name("Nieistniejąca")

    # Assert
    assert result is None

def test_delete_gender_by_id(repository, sample_genders):
    # Arrange
    mock_read = mock_open(read_data=json.dumps(sample_genders))
    mock_write = mock_open()
    combined_mock = Mock()
    combined_mock.side_effect = [mock_read.return_value, mock_write.return_value]

    # Act
    with patch('builtins.open', combined_mock):
        repository.delete_gender_by_id(1)

    # Assert
    write_calls = combined_mock.call_args_list
    assert len(write_calls) == 2
    assert write_calls[1][0][1] == 'w'