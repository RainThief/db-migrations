*** Settings ***


Documentation    Resource file for the count sesame test suite


Library    OperatingSystem
Library    logging
Library    robot.api.logger     WITH NAME    log
Library    test.lib.logger
Library    test.lib.postgres_container    WITH NAME    postgres_container
Library    test.lib.alembic    WITH NAME    alembic
Library    test.lib.database    WITH NAME    database
Library    test.lib.database.DatabaseConnection



*** Variables ***


${DB_IMAGE}    postgres:12
${DB_URL}    postgresql://user:password@127.0.0.1:5432/db
${LOG_FILE_PATH}    logs/developer_log.txt



*** Keywords ***


SuiteSetup
    log.info    Suite Setup
    # log level declared in cli args
    test.lib.logger.set_level    ${LOG_LEVEL}
    test.lib.logger.set_file_path    ${LOG_FILE_PATH}
    test.lib.database.DatabaseConnection.set_url    ${DB_URL}


SuiteTeardown
    # sigint runs teardown, stop any containers running
    postgres_container.stop


TestTeardown
    log.info    Test Teardown for: ${TEST_NAME} - ${TEST_TAGS}
    test.lib.database.DatabaseConnection.close
    postgres_container.stop


Given an empty database is ready and accepting connections
    postgres_container.start    ${DB_IMAGE}


When migrate is ran with direction ${direction} and revison id ${revison_id}
    alembic.migrate    ${direction}    ${revison_id}    ${DB_URL}


Then the database will have a table called ${tbl_name}
    test.lib.database.DatabaseConnection.call    check_table_exists    ${tbl_name}
    # database.check_table_exists    ${tbl_name}


Then the database will NOT have a table called ${tbl_name}
    test.lib.database.DatabaseConnection.call    check_table_not_exists    ${tbl_name}


And the ${tbl_name} table will have a columns named ${columns}
    database.check_column_names    ${tbl_name}    ${columns}


And the database is seeded
    database.seed


And the ${tbl_name} table will have ${num_records} records
    test.lib.database.DatabaseConnection.call    check_record_count    ${tbl_name}    ${num_records}


And the ${first} record from ${tbl_name} table will have a value of ${value} in the ${column} column
    test.lib.database.DatabaseConnection.call    check_record_by_position    ${first}    ${tbl_name}    ${column}    ${value}


And seed enviroment is set
    Set Environment Variable    SEED    true
